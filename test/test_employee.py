import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


#POSITIVE TEST CASES


def test_get_all_employees_positive():
    with TestClient(app) as client:
        response = client.get("/employees/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_create_employee_positive():
    new_employee = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "phone_number": "1234567890",
        "hire_date": "2024-01-01",
        "job_id": "DEV1",
        "salary": 70000.0,
        "department_id": 101
    }
    with TestClient(app) as client:
        response = client.post("/employees/", json=new_employee)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["first_name"] == new_employee["first_name"]
        assert "employee_id" in data

def test_get_employee_by_id_positive():
    new_employee = {
        "first_name": "Get",
        "last_name": "User",
        "email": "getuser@example.com",
        "phone_number": "1234567891",
        "hire_date": "2024-01-02",
        "job_id": "QA1",
        "salary": 60000.0,
        "department_id": 202
    }
    with TestClient(app) as client:
        post_response = client.post("/employees/", json=new_employee)
        emp_id = post_response.json()["employee_id"]

        response = client.get(f"/employees/{emp_id}")
        assert response.status_code == 200
        assert response.json()["email"] == new_employee["email"]

def test_search_by_department_positive():
    with TestClient(app) as client:
        response = client.get("/employees/search", params={"department_id": 101})
        assert response.status_code == 200
        assert isinstance(response.json(), list)


#  NEGATIVE TEST CASES

def test_get_employee_by_invalid_id():
    with TestClient(app) as client:
        response = client.get("/employees/999999")  # ID doesn't exist
        assert response.status_code == 404
        assert response.json()["detail"] == "Employee not found"


def test_create_employee_missing_field():
    incomplete_employee = {
        "first_name": "Invalid",
        # Missing last_name, email, phone_number, etc.
        "hire_date": "2024-01-01",
        "job_id": "DEV2",
        "salary": 50000.0,
        "department_id": 105
    }
    with TestClient(app) as client:
        response = client.post("/employees/", json=incomplete_employee)
        assert response.status_code == 422  # Unprocessable Entity

def test_search_without_params():
    with TestClient(app) as client:
        response = client.get("/employees/search")  # no query params
        assert response.status_code == 422
        assert "At least one filter" in response.json()["detail"]

def test_search_invalid_department():
    with TestClient(app) as client:
        response = client.get("/employees/search", params={"department_id": 9999})
        assert response.status_code == 404
        assert response.json()["detail"] == "No employees found for the given filters"
