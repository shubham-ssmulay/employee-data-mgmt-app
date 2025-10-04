"""
FastAPI entry point for Employee CRUD app.
"""
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from typing import List
from contextlib import asynccontextmanager


from utils.database import create_db_and_tables, get_session
from models.employee import EmployeeRead, EmployeeCreate, EmployeeUpdate
from crud.crud import EmployeeCRUD

# ------------------------
# Initialize FastAPI
# ------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up API service...")
    create_db_and_tables()

    yield  # Control is given to FastAPI here

    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan, title="Employee CRUD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # FE port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Router with base path
# ------------------------
router = APIRouter(prefix="/api/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeRead)
def create_employee(employee: EmployeeCreate, session: Session = Depends(get_session)):
    return EmployeeCRUD.create(session, employee)

@router.get("/", response_model=List[EmployeeRead])
def list_employees(q: str = "", session: Session = Depends(get_session)):
    return EmployeeCRUD.get_all(session, q)

@router.get("/{emp_id}", response_model=EmployeeRead)
def get_employee(emp_id: int, session: Session = Depends(get_session)):
    return EmployeeCRUD.get(session, emp_id)

@router.put("/{emp_id}", response_model=EmployeeRead)
def update_employee(emp_id: int, payload: EmployeeUpdate, session: Session = Depends(get_session)):
    return EmployeeCRUD.update(session, emp_id, payload)

@router.delete("/{emp_id}")
def delete_employee(emp_id: int, session: Session = Depends(get_session)):
    return EmployeeCRUD.delete(session, emp_id)

# ------------------------
# Register router
# ------------------------
app.include_router(router)
