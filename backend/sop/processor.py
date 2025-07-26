import os
import uuid
import hashlib
import pickle
import traceback
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import (PyMuPDFLoader, Docx2txtLoader, TextLoader)

load_dotenv()

# Constants
VECTOR_STORE_PATH = "faiss_store"
INDEX_FILE = os.path.join(VECTOR_STORE_PATH, "index.faiss")
METADATA_PATH = os.path.join(VECTOR_STORE_PATH, "doc_metadata.pkl")

# Embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def get_loader(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return PyMuPDFLoader(file_path)
    elif ext == ".docx":
        return Docx2txtLoader(file_path)
    elif ext == ".txt":
        return TextLoader(file_path)
    else:
        raise ValueError(f"❌ Unsupported file type: {ext}")

# Metadata store (for filenames & hashes)
def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "rb") as f:
            return pickle.load(f)
    return {}

def save_metadata(metadata):
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

# File hashing function
def compute_file_hash(file_path):
    hash_func = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# Main processor
def process_document(file_path):
    try:
        loader = get_loader(file_path)
    except ValueError as e:
        return str(e)

    try:
        print(f"📄 Loading document: {file_path}")
        documents = loader.load()
        print("✅ Document loaded successfully")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"❌ Error loading document: {e}"

    file_hash = compute_file_hash(file_path)
    metadata = load_metadata()

    # 🚫 Skip if hash already exists
    if file_hash in metadata.values():
        return f"⚠️ File already exists in vector store. Skipping: {os.path.basename(file_path)}"

    doc_id = str(uuid.uuid4())
    for doc in documents:
        doc.metadata["doc_id"] = doc_id
        doc.metadata["source"] = os.path.basename(file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    if os.path.exists(INDEX_FILE):
        db = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)
        db.add_documents(chunks)
    else:
        db = FAISS.from_documents(chunks, embedding_model)

    db.save_local(VECTOR_STORE_PATH)

    metadata[doc_id] = file_hash
    save_metadata(metadata)

    return f"✅ Added '{file_path}' to vector store."


# Delete PDF from vector store
def delete_document(file_name):
    if not os.path.exists(VECTOR_STORE_PATH):
        return "⚠️ No vector store found."

    db = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)
    metadata = load_metadata()

    # Get doc_id for this file
    doc_ids_to_remove = [doc_id for doc_id, fname in metadata.items() if fname == file_name]
    if not doc_ids_to_remove:
        return f"❌ No document found with filename: {file_name}"

    # Filter documents not matching the doc_id(s)
    original_docs = db.docstore._dict
    updated_docs = {k: v for k, v in original_docs.items() if v.metadata.get("doc_id") not in doc_ids_to_remove}

    # Rebuild FAISS
    db = FAISS.from_documents(list(updated_docs.values()), embedding_model)
    db.save_local(VECTOR_STORE_PATH)

    # Update metadata
    for doc_id in doc_ids_to_remove:
        del metadata[doc_id]
    save_metadata(metadata)

    return f"🗑️ Removed '{file_name}' from vector store."

# Query
def query_index(question):
    try:
        print(f"[DEBUG] Checking vector store path: {VECTOR_STORE_PATH}")
        if not os.path.exists(VECTOR_STORE_PATH):
            raise FileNotFoundError("⚠️ No vector index found. Please add documents first.")

        print("[DEBUG] Loading FAISS vector store...")
        db = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)

        print("[DEBUG] Getting retriever...")
        retriever = db.as_retriever()

        print("[DEBUG] Initializing OpenAI Chat model...")
        llm = ChatOpenAI(
            model="gpt-4.1-mini",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.5
        )

        print("[DEBUG] Creating RetrievalQA chain...")
        chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

        print("[DEBUG] Invoking chain...")
        result = chain.invoke({"query": question})
        return result["result"]

    except Exception as e:
        print("[ERROR] Exception in query_index()")
        traceback.print_exc()
        raise e

