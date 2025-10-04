"""
Employee SQLAlchemy model and Pydantic schemas with is_active flag.
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


# Pydantic Schemas
class EmployeeBase(BaseModel):
    name: str
    email: str
    position: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    position: str | None = None


class EmployeeRead(EmployeeBase):
    id: int
    is_active: bool


class Config:
    orm_mode = True