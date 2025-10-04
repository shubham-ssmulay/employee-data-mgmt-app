import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app, get_db
from models.employee import Base

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ------------------------
# Tests
# ------------------------

def test_create_employee():
    payload = {"name": "Alice", "email": "alice@test.com", "position": "Developer"}
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@test.com"

def test_create_duplicate_email():
    payload = {"name": "Bob", "email": "alice@test.com", "position": "Tester"}
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_employees():
    response = client.get("/api/employees")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(emp["email"] == "alice@test.com" for emp in data)

def test_update_employee():
    # Get ID of first employee
    employees = client.get("/api/employees").json()
    emp_id = employees[0]["id"]
    payload = {"name": "Alice Updated", "position": "Lead"}
    response = client.put(f"/api/employees/{emp_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice Updated"

def test_soft_delete_employee():
    employees = client.get("/api/employees").json()
    emp_id = employees[0]["id"]
    response = client.delete(f"/api/employees/{emp_id}")
    assert response.status_code == 200
    # Employee should not appear in get_all
    employees_after = client.get("/api/employees").json()
    assert all(emp["id"] != emp_id for emp in employees_after)

def test_restore_employee():
    # Soft-deleted employee ID = 1
    response = client.post("/api/employees/1/restore")
    assert response.status_code == 200
    # Now should appear in list
    employees_after = client.get("/api/employees").json()
    assert any(emp["id"] == 1 for emp in employees_after)
