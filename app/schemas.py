from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    hire_date: date
    job_id: str
    salary: float
    department_id: int

class EmployeeCreate(EmployeeBase):
    pass
class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    hire_date: Optional[date] = None
    job_id: Optional[str] = None
    salary: Optional[float] = None
    department_id: Optional[int] = None

class Employee(EmployeeBase):
    employee_id: int

    class Config:
        orm_mode = True
