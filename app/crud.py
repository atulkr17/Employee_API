# from .database import database
# from .moddels import employee
# from .schemas import EmployeeCreate
# from .schemas import EmployeeUpdate
# from typing import Optional

# async def create_employee(data: EmployeeCreate):
#     query = employee.insert().values(
#         first_name=data.first_name,
#         last_name=data.last_name,
#         email=data.email,
#         phone_number=data.phone_number,
#         hire_date=data.hire_date,
#         job_id=data.job_id,
#         salary=data.salary,
#         department_id=data.department_id
#     )
#     emp_id = await database.execute(query)
#     return {**data.dict(), "employee_id": emp_id}

# async def get_employees():
#     query = employee.select()
#     return await database.fetch_all(query)

# async def get_employee(emp_id: int):
#     query = employee.select().where(employee.c.employee_id == emp_id)
#     return await database.fetch_one(query)

# async def delete_employee(emp_id: int):
#     query = employee.delete().where(employee.c.employee_id == emp_id)
#     return await database.execute(query)
# async def update_employee(emp_id: int, data: EmployeeUpdate):
#     update_data = data.dict(exclude_unset=True)
#     query = employee.update().where(employee.c.employee_id == emp_id).values(**update_data)
#     await database.execute(query)
#     return await get_employee(emp_id)

# async def search_employees(department_id: Optional[int] = None, job_id: Optional[str] = None):
#     query = employee.select()

#     if department_id is not None:
#         query = query.where(employee.c.department_id == department_id)
#     if job_id is not None:
#         query = query.where(employee.c.job_id == job_id)

#     return await database.fetch_all(query)

from .database import database
from .moddels import employee
from .schemas import EmployeeCreate, EmployeeUpdate
from typing import Optional
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def create_employee(data: EmployeeCreate):
    try:
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
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        raise HTTPException(status_code=500, detail="Error creating employee")

async def get_employees():
    try:
        query = employee.select()
        return await database.fetch_all(query)
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        raise HTTPException(status_code=500, detail="Error fetching employee data")

async def get_employee(emp_id: int):
    # try:
    #     query = employee.select().where(employee.c.employee_id == emp_id)
    #     employee_data = await database.fetch_one(query)
    #     if not employee_data:
    #         raise HTTPException(status_code=404, detail="Employee not found")
    #     return employee_data
    # except HTTPException:
    #     raise
    # except Exception as e:
    #     logger.error(f"Error fetching employee by ID: {e}")
    #     raise HTTPException(status_code=500, detail="Error fetching employee")
    try:
        query = employee.select().where(employee.c.employee_id == emp_id)
        result = await database.fetch_one(query)
        return result  # will be None if not found
    except Exception as e:
        # Log if needed: print(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_employee(emp_id: int):
    try:
        query = employee.delete().where(employee.c.employee_id == emp_id)
        result = await database.execute(query)
        return result
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        raise HTTPException(status_code=500, detail="Error deleting employee")

async def update_employee(emp_id: int, data: EmployeeUpdate):
    try:
        update_data = data.dict(exclude_unset=True)
        query = employee.update().where(employee.c.employee_id == emp_id).values(**update_data)
        await database.execute(query)
        return await get_employee(emp_id)
    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        raise HTTPException(status_code=500, detail="Error updating employee")

async def search_employees(department_id: Optional[int] = None, job_id: Optional[str] = None):
    try:
        query = employee.select()
        if department_id:
            query = query.where(employee.c.department_id == department_id)
        if job_id:
            query = query.where(employee.c.job_id == job_id)

        results = await database.fetch_all(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database search error: {str(e)}")