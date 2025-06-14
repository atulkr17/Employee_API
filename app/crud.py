from .database import database
from .moddels import employee
from .schemas import EmployeeCreate
from .schemas import EmployeeUpdate
from typing import Optional

async def create_employee(data: EmployeeCreate):
    query = employee.insert().values(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone_number=data.phone_number,
        hire_date=data.hire_date,
        job_id=data.job_id,
        salary=data.salary,
        department_id=data.department_id
    )
    emp_id = await database.execute(query)
    return {**data.dict(), "employee_id": emp_id}

async def get_employees():
    query = employee.select()
    return await database.fetch_all(query)

async def get_employee(emp_id: int):
    query = employee.select().where(employee.c.employee_id == emp_id)
    return await database.fetch_one(query)

async def delete_employee(emp_id: int):
    query = employee.delete().where(employee.c.employee_id == emp_id)
    return await database.execute(query)
async def update_employee(emp_id: int, data: EmployeeUpdate):
    update_data = data.dict(exclude_unset=True)
    query = employee.update().where(employee.c.employee_id == emp_id).values(**update_data)
    await database.execute(query)
    return await get_employee(emp_id)

async def search_employees(department_id: Optional[int] = None, job_id: Optional[str] = None):
    query = employee.select()

    if department_id is not None:
        query = query.where(employee.c.department_id == department_id)
    if job_id is not None:
        query = query.where(employee.c.job_id == job_id)

    return await database.fetch_all(query)