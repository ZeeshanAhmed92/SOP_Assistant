# 🧠 Audio SOP Assistant

A cross-platform mobile application built with **React Native** and a **Flask** backend that allows employees to ask voice-based SOP questions during their shift and get AI-powered responses.

---

## 📆 Features

- 🔒 Secure JWT-based login with role control (Admin / Employee)
- 🗓️ Shift-based access control (only on-duty employees can use assistant)
- 🡩‍💼 Admin dashboard to upload SOPs (PDF/JSON) and manage schedules
- 🎙️ Voice input using Speech-to-Text (STT)
- 🔈 AI responses read back using Text-to-Speech (TTS)
- 🔍 RAG-based SOP assistant (via vector index and OpenAI GPT)
- 📊 Logging of all usage and interactions

---

## 🧠 Tech Stack

| Layer      | Tech Used                           |
| ---------- | ----------------------------------- |
| Frontend   | React Native (Expo)                 |
| Backend    | Flask, Gunicorn                     |
| AI         | OpenAI GPT + FAISS (RAG model)      |
| Audio      | gTTS (TTS), SpeechRecognition (STT) |
| Database   | PostgreSQL                          |
| Deployment | Docker, Docker Compose, NGINX       |

---

## 🚀 Getting Started

### 🐳 Backend (Flask + PostgreSQL)

```bash
# Build and run backend + DB
docker-compose up --build
```

### 📱 Frontend (React Native)

```bash
cd frontend
npm install
npx expo start
```

> Make sure to update `api.js` with your backend IP or domain.

---

## 📁 Project Structure

```
project-root/
├── backend/             # Flask backend
│   ├── auth/            # Auth endpoints & JWT
│   ├── audio/           # STT & TTS routes
│   ├── employees/       # Models, shift validation, CRUD
│   ├── logs/            # SOP + access logs
│   ├── sop/             # Upload, query, RAG interface
│   └── app.py           # Entrypoint
├── frontend/            # React Native app
│   ├── screens/         # Login, EmployeeHome, AdminDashboard
│   ├── components/      # AudioRecorder, AudioPlayer
│   └── utils/           # Token storage & decoding
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🔐 Environment Variables

In production, configure your Flask container:

```env
SECRET_KEY=your-secret
DATABASE_URL=postgresql://postgres:postgres@db:5432/audio_sop
```

---

## 📌 To-Do / Enhancements

-

