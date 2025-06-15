from fastapi import FastAPI, HTTPException
from .database import database, metadata
from .schemas import EmployeeCreate, Employee
from . import crud
import sqlalchemy
from .schemas import EmployeeUpdate
from fastapi import HTTPException, Query
from typing import Optional
from contextlib import asynccontextmanager

# Use sync SQLAlchemy engine to create table if not exists
engine = sqlalchemy.create_engine(str(database.url).replace("+asyncpg", ""))
metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

@app.post("/employees/", response_model=Employee)
async def create(data: EmployeeCreate):
    return await crud.create_employee(data)

# @app.get("/employees/", response_model=list[Employee])
# async def read_all():
#     return await crud.get_employees()



@app.delete("/employees/{emp_id}")
async def delete(emp_id: int):
    await crud.delete_employee(emp_id)
    return {"message": f"Employee with ID {emp_id} deleted"}


@app.put("/employees/{emp_id}", response_model=Employee)
async def update(emp_id: int, data: EmployeeUpdate):
    existing = await crud.get_employee(emp_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Employee not found")
    return await crud.update_employee(emp_id, data)

@app.get("/employees/", response_model=list[Employee])
async def get_all_employees():
    return await crud.get_employees()

@app.get("/employees/search", response_model=list[Employee])
async def search_employees(
    department_id: Optional[int] = Query(default=None),
    job_id: Optional[str] = Query(default=None)
):
    if department_id is None and job_id is None:
        raise HTTPException(status_code=422, detail="At least one filter (department_id or job_id) must be provided.")

    results = await crud.search_employees(department_id, job_id)
    if not results:
        raise HTTPException(status_code=404, detail="No employees found for the given filters")
    return results
@app.get("/employees/{emp_id}", response_model=Employee)
async def read_one(emp_id: int):
    result = await crud.get_employee(emp_id)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result
