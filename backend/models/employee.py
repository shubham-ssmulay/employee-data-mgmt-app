"""
Employee SQLAlchemy model and Pydantic schemas with is_active flag and position enum.
"""

from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

Base = declarative_base()


# Enum for allowed positions
class PositionEnum(str, Enum):
    software_engineer = "Software Engineer"
    data_engineer = "Data Engineer"
    ml_engineer = "ML Engineer"
    quality_analyst = "Quality Analyst"
    solutions_architect = "Solutions Architect"
    sales_representative = "Sales Representative"


# SQLAlchemy model
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


# ───────────────────────────────
# Pydantic Schemas
# ───────────────────────────────

class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    position: PositionEnum

    class Config:
        orm_mode = True


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee."""
    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating employee fields (partial)."""
    name: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    position: Optional[PositionEnum] = None

    class Config:
        orm_mode = True


class EmployeeRead(EmployeeBase):
    """Schema for reading employee data."""
    id: int
    is_active: bool

    class Config:
        orm_mode = True
