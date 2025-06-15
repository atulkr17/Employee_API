import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_all_employees():
    with TestClient(app) as client:
        response = client.get("/employees/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# def test_create_employee():
#     new_employee = {
#         "first_name": "Test",
#         "last_name": "User",
#         "email": "testuser@example.com",
#         "phone_number": "1234567890",
#         "hire_date": "2024-01-01",
#         "job_id": "DEV1",
#         "salary": 70000.0,
#         "department_id": 101
#     }
#     with TestClient(app) as client:
#         response = client.post("/employees/", json=new_employee)
#         assert response.status_code == 200 or response.status_code == 201
#         data = response.json()
#         assert data["first_name"] == new_employee["first_name"]
#         assert "employee_id" in data  # check id returned


# def test_get_employee_by_id():
#     # First create an employee
#     new_employee = {
#         "first_name": "Get",
#         "last_name": "User",
#         "email": "getuser@example.com",
#         "phone_number": "1234567891",
#         "hire_date": "2024-01-02",
#         "job_id": "QA1",
#         "salary": 60000.0,
#         "department_id": 202
#     }
#     with TestClient(app) as client:
#         post_response = client.post("/employees/", json=new_employee)
#         emp_id = post_response.json()["employee_id"]

#         # Now fetch by ID
        
#         response = client.get(f"/employees/{emp_id}")
#         assert response.status_code == 200
#         assert response.json()["email"] == "getuser@example.com"


def test_search_by_department():
    with TestClient(app) as client:
        # Make sure employee with department_id 101 exists before this
        response = client.get("/employees/search", params={"department_id": "101"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)

