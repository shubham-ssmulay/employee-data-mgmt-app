1️⃣ backend/README.md
# Employee Manager Backend

## Overview
Backend service for Employee Manager using **FastAPI** and **SQLAlchemy**.  
Supports CRUD operations with **soft delete** (`is_active` flag) and logs actions using **loguru**.

---

## Requirements
- Python 3.10+  
- Install dependencies:
```bash
pip install -r requirements.txt
```

Example requirements.txt:

fastapi
uvicorn
sqlalchemy
pydantic
loguru

Directory Structure
```
backend/
├── crud/
│   └── crud.py
├── models/
│   └── employee.py
├── src/
│   └── main.py
├── utils/
│   └── database.py
└── tests/
```

# Run Backend
From backend directory run below command - 

```
cd <backend_directory>
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```


Swagger URL: 

http://localhost:8000/docs



