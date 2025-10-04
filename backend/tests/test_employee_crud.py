import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app, get_session  # adjust if your import path differs
from models.employee import Base       # adjust if your import path differs

# Create an in-memory SQLite DB engine for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:tests.db:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # ensures same connection is used for the whole test session
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables before tests start
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a FastAPI test client that overrides the DB dependency."""
    def override_get_session():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_employee(client):
    payload = {
        "name": "Alice",
        "email": "alice@test.com",
        "position": "Software Engineer"  # 👈 must match PositionEnum
    }
    response = client.post("/api/employees/", json=payload)
    assert response.status_code == 200


def test_create_duplicate_email(client):
    # First, create Alice
    payload = {
        "name": "Alice", 
        "email": "alice@test.com", 
        "position": "Software Engineer"
    }
    client.post("/api/employees/", json=payload)

    # Try creating Bob with Alice's email
    payload = {
        "name": "Bob", 
        "email": "alice@test.com", 
        "position": "ML Engineer"
    }
    response = client.post("/api/employees/", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_employees(client):
    # Insert employee first
    payload = {
        "name": "Alice", 
        "email": "alice@test.com", 
        "position": "Quality Analyst"
    }
    client.post("/api/employees/", json=payload)

    response = client.get("/api/employees/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(emp["email"] == "alice@test.com" for emp in data)


def test_update_employee(client):
    # Insert employee first
    payload = {
        "name": "Alice", 
        "email": "alice@test.com", 
        "position": "Data Engineer"
    }
    client.post("/api/employees/", json=payload)

    employees = client.get("/api/employees/").json()
    emp_id = employees[0]["id"]

    update_payload = {
        "name": "Alice Updated", 
        "position": "ML Engineer"
    }
    response = client.put(f"/api/employees/{emp_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice Updated"


def test_soft_delete_employee(client):
    # Insert employee first
    payload = {
        "name": "Alice", 
        "email": "alice@test.com", 
        "position": "Data Engineer"
    }
    client.post("/api/employees/", json=payload)

    employees = client.get("/api/employees/").json()
    emp_id = employees[0]["id"]

    response = client.delete(f"/api/employees/{emp_id}")
    assert response.status_code == 200

    employees_after = client.get("/api/employees/").json()
    assert all(emp["id"] != emp_id for emp in employees_after)


# def test_restore_employee(client):
#     # Insert employee first
#     payload = {"name": "Alice", "email": "alice@test.com", "position": "Developer"}
#     client.post("/api/employees/", json=payload)

#     employees = client.get("/api/employees/").json()
#     emp_id = employees[0]["id"]

#     # Soft delete
#     client.delete(f"/api/employees/{emp_id}")

#     # Add a restore endpoint in your API if missing!
#     response = client.post(f"/api/employees/{emp_id}/restore")
#     assert response.status_code == 200

#     employees_after = client.get("/api/employees/").json()
#     assert any(emp["id"] == emp_id for emp in employees_after)
