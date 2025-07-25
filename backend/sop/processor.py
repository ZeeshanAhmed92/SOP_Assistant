import os
import uuid
import pickle
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()


from langchain_community.document_loaders import (
    PyMuPDFLoader,           # PDF
    Docx2txtLoader,          # DOCX
    TextLoader               # TXT
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


# Constants
VECTOR_STORE_PATH = "faiss_store"
METADATA_PATH = os.path.join(VECTOR_STORE_PATH, "doc_metadata.pkl")

# Embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=os.getenv('OPENAI_API_KEY')
)

# Metadata store
def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "rb") as f:
            return pickle.load(f)
    return {}

def save_metadata(metadata):
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)



# Add new PDF to vector store
def process_document(file_path):
    print("processing doc")
    try:
        loader = get_loader(file_path)
    except ValueError as e:
        return str(e)
    print("about to load doc")
    try:
        print(f"📄 Loading document: {file_path}")
        documents = loader.load()
        print("✅ Document loaded successfully")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"❌ Error loading document: {e}"
    doc_id = str(uuid.uuid4())
    print("set id doc")
    for doc in documents:
        doc.metadata["doc_id"] = doc_id
        doc.metadata["source"] = os.path.basename(file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print("chunked doc")
    if os.path.exists(VECTOR_STORE_PATH):
        db = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)
        db.add_documents(chunks)
    else:
        db = FAISS.from_documents(chunks, embedding_model)

    db.save_local(VECTOR_STORE_PATH)

    metadata = load_metadata()
    metadata[doc_id] = os.path.basename(file_path)
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
    if not os.path.exists(VECTOR_STORE_PATH):
        return "⚠️ No vector index found. Please add documents first."

    db = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()

    llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

    result = chain.invoke({"query": question})
    return result["result"]
