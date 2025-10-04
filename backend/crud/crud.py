"""
CRUD operations for Employee using SQLAlchemy with is_active flag (soft delete).
"""
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from loguru import logger
from sqlalchemy.exc import IntegrityError



from models.employee import Employee, EmployeeCreate, EmployeeUpdate


class EmployeeCRUD:
    @staticmethod
    def create(db: Session, emp: EmployeeCreate) -> Employee:
        logger.info("Creating new employee: {}", emp.email)
        db_emp = Employee(**emp.model_dump())
        try:
            db.add(db_emp)
            db.commit()
            db.refresh(db_emp)
        except IntegrityError:
            db.rollback()
            logger.error("Employee with email {} already exists", emp.email)
            raise HTTPException(status_code=400, detail="Employee with this email already exists")
        except Exception:
            db.rollback()
            logger.error(f"Error is creating employee")
            raise HTTPException(status_code=500, detail="Error is creating employee")
        return db_emp


    @staticmethod
    def get_all(db: Session, q: str = "") -> List[Employee]:
        logger.info("Fetching employees (filter={})", q)
        query = db.query(Employee).filter(Employee.is_active == True)
        if q:
            query = query.filter(Employee.name.ilike(f"%{q}%"))
        return query.all()


    @staticmethod
    def get(db: Session, emp_id: int) -> Employee:
        emp = db.query(Employee).filter(Employee.id == emp_id, Employee.is_active == True).first()
        if not emp:
            logger.warning("Employee {} not found", emp_id)
            raise HTTPException(status_code=404, detail="Employee not found")
        return emp


    @staticmethod
    def update(db: Session, emp_id: int, payload: EmployeeUpdate) -> Employee:
        emp = db.query(Employee).filter(Employee.id == emp_id, Employee.is_active == True).first()
        if not emp:
            logger.warning("Update failed. Employee {} not found", emp_id)
            raise HTTPException(status_code=404, detail="Employee not found")

        for key, val in payload.model_dump(exclude_unset=True).items():
            setattr(emp, key, val)
            db.add(emp)
            db.commit()
            db.refresh(emp)
            logger.info("Updated employee {}", emp_id)
        return emp


    @staticmethod
    def delete(db: Session, emp_id: int):
        emp = db.query(Employee).filter(Employee.id == emp_id, Employee.is_active == True).first()
        if not emp:
            logger.warning("Delete failed. Employee {} not found", emp_id)
            raise HTTPException(status_code=404, detail="Employee not found")

        emp.is_active = False
        db.add(emp)
        db.commit()
        logger.info("Soft deleted (deactivated) employee {}", emp_id)
        return {"ok": True, "message": "Employee deleted"}