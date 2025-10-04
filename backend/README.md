# 📘 Employee Management System – Backend

This is the **backend** service for the Employee Management System built with **FastAPI** and **SQLAlchemy**.  
It supports full CRUD functionality with **soft delete** (`is_active` flag) and uses **Loguru** for structured logging.

---

## 🚀 Features

- Create, read, update, and soft-delete employees.
- Search by employee name.
- API docs with Swagger UI.
- Modular structure with models, CRUD logic, and utilities.
- Logging with `loguru`.

---

## ⚙️ Requirements
Python 3.10+

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

# Project Structure

```
backend/
├── README.md                   → You're here
├── requirements.txt
├── tox.ini                     → For running tests with pytest + coverage
├── crud/
│   └── crud.py                 → Business logic for employees
├── models/
│   ├── __init__.py
│   └── employee.py             → SQLAlchemy model + Pydantic schemas
├── src/
│   ├── __init__.py
│   └── main.py                 → FastAPI app and routes
├── utils/
│   └── database.py             → DB session + engine setup
└── tests/
    └── test_employee_crud.py   → API and logic tests
```

# ▶️ Run the Backend Server

```
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be live at - http://localhost:8000

## API Documentation

FastAPI provides interactive Swagger docs at:

📄 http://localhost:8000/docs

🧾 ReDoc (alternative): http://localhost:8000/redoc

# Run Tests

```
cd backend
export PYTHONPATH=.
pytest
```

Or with coverage (via tox):
```
tox
```

### Notes
1. Uses an is_active boolean field to implement soft delete.
2. Make sure the database is set up before running the app (can be SQLite or any other SQLAlchemy-supported DB).