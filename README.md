
---

## **3️⃣ Root-level README.md**


# Employee Manager Fullstack Project

## Overview
Simple CRUD application for managing employees:

- **Backend:** FastAPI + SQLAlchemy + SQLite  
- **Frontend:** React + Vite + Tailwind CSS  
- Features:
  - Create / Read / Update / Soft Delete / Restore  
  - Search employees by name  
  - Field validation & unique email enforcement  

---

## Prerequisites
- Python 3.10+  
- Node.js 18+  

---

## Setup & Run

### 1️⃣ Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API base URL: `http://localhost:8000/api/employees`

### 2️⃣ Frontend
```
cd frontend
npm install
npm run dev
```

Frontend default URL: `http://localhost:5173` (proxies API to backend)



# How to run on local

```
bash local_run.sh
```