from sqlalchemy import Table, Column, Integer, String, Numeric, Date
from .database import metadata

employee = Table(
    "employee",
    metadata,
    Column("employee_id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("email", String(100)),
    Column("phone_number", String(20)),
    Column("hire_date", Date),
    Column("job_id", String(10)),
    Column("salary", Numeric(10, 2)),
    Column("department_id", Integer)
)
