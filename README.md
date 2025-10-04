# Employee Data Management — Fullstack Project

## Overview
A simple *full-stack CRUD application* to manage employee data efficiently.

*Stack:*
- *Backend:* FastAPI + SQLAlchemy + SQLite  
- *Frontend:* React + Vite + Tailwind CSS  
- *Features:*
  - Create / Read / Update / Soft Delete  
  - Search employees by name  
  - Field validation and unique email enforcement  
  - Modular architecture with test coverage (Pytest + Jest)

---

## ⚙️ Prerequisites
Before running the project, ensure you have:
- *Python 3.10+*
- *Node.js 18+*
- *npm* or *yarn*

---

## 🚀 Setup & Run Instructions

You can run backend and frontend *separately* or *together* using a helper script.

---

### 1️⃣ Run Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API Base URL: http://localhost:8000/api/employees

Swagger Docs available at: http://localhost:8000/docs

### 2️⃣ Run Frontend (React)
```bash
cd frontend
npm install
npm run dev
```


Frontend default URL: http://localhost:5173

(The frontend proxies all /api/employees calls to the FastAPI backend.)

### 3️⃣ Unified Local Run

To start both frontend and backend together:

```bash
bash local_run.sh
```

This will:

Start FastAPI on port 8000

Start Vite dev server on port 5173

Ensure proper CORS configuration

### Running Tests

## Backend Tests (Pytest)

```bash
cd backend
export PYTHONPATH=.
pytest
```

Make sure $PYTHONPATH is set to . before running tests.

Includes unit + integration tests for CRUD operations.

## Frontend Tests (Jest + React Testing Library)

```bash
cd frontend
npm test
```

Tests rendering, validation, modal behavior, and CRUD UI flow.

Mocks backend API for consistent results.

# Design Choices & Architecture


### Overall Architecture

Monorepo structure with separate frontend and backend directories.

Clear modular separation for scalability and maintainability.

```
project/
├── backend/
│   ├── crud/
│   ├── models/
│   ├── src/
│   ├── utils/
│   └── tests/
└── frontend/
```

### Backend (FastAPI + SQLAlchemy)


1. Framework: FastAPI
  - Modern, high-performance Python web framework.
  - Built-in type validation with Pydantic.
  - Auto-generated interactive API docs (/docs).

2. Database: SQLite via SQLAlchemy
- Chosen for simplicity and portability.
- Easy migration path to PostgreSQL/MySQL later.
- ORM ensures model consistency and easier testing.

3. Soft Delete vs Hard Delete
- Decision: Implemented soft delete (is_active flag).
  - Prevents accidental data loss.
  - Allows quick reactivation if an employee rejoins.
  - Preserves historical data for auditing.

4. Modular CRUD Layer
- Centralized CRUD logic inside crud/crud.py.
- Keeps API routes clean and focuses on data access separation.

5. Error Handling
- Consistent HTTP responses using HTTPException.
- Returns human-readable messages for the frontend.

6. Logging
- Loguru integrated for structured and colorized logs.
- Logs all lifecycle events — startup, CRUD operations, and errors.

7. CORS & API Base Path
- API base path: /api/employees for RESTful clarity.
- CORS configured to allow frontend access from http://localhost:5173.

### Frontend (React + Vite + Tailwind)

1. Framework: React (with Hooks)
- Uses functional components and useState/useEffect hooks.
- Simple state management (no external state library).

2. UI: Tailwind CSS
- Utility-first CSS framework for rapid, consistent UI design.
- Enables responsive and clean layouts with minimal code.

3. Data Flow
- Uses the fetch API for REST calls to the backend.
- Handles loading, success, and error states gracefully.

4. Modular Components
- Components separated for EmployeeTable, EmployeeModal, etc.
- Improves testability and readability.

5. Validation
- Frontend form validation (empty fields, duplicate email handling).
- Backend re-verifies for data consistency.


### Testing Design


Backend:
  - Uses Pytest + FastAPI TestClient.
  - Unit tests for CRUD logic and integration for routes.

Frontend:
  - Uses Jest + React Testing Library.
  - Tests user interactions (add/edit/delete) and UI behavior.