import pytest
from fastapi.testclient import TestClient
from app.vehicle_api import app
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

# Recreate the database for testing
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def clear_db():
    """Clear DB before each test."""
    db: Session = SessionLocal()
    db.query(Base.metadata.tables['vehicles']).delete()
    db.commit()
    db.close()

def test_register_vehicle_success():
    response = client.post("/register", json={"plate_number": "GJ01AB1234", "balance": 100})
    assert response.status_code == 201
    assert response.json()["plate_number"] == "GJ01AB1234"
    assert response.json()["balance"] == 100

def test_register_vehicle_duplicate():
    client.post("/register", json={"plate_number": "GJ01AB1234", "balance": 100})
    response = client.post("/register", json={"plate_number": "GJ01AB1234", "balance": 200})
    assert response.status_code == 400
    assert response.json()["detail"] == "Vehicle already registered"

def test_top_up_success():
    client.post("/register", json={"plate_number": "GJ01XY7890", "balance": 50})
    response = client.post("/topup/GJ01XY7890", json={"amount": 70})
    assert response.status_code == 200
    assert response.json()["balance"] == 120

def test_top_up_vehicle_not_found():
    response = client.post("/topup/GJ99ZZ9999", json={"amount": 50})
    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"

def test_get_balance_success():
    client.post("/register", json={"plate_number": "GJ02CD5678", "balance": 300})
    response = client.get("/balance/GJ02CD5678")
    assert response.status_code == 200
    assert response.json()["plate_number"] == "GJ02CD5678"

def test_get_balance_vehicle_not_found():
    response = client.get("/balance/GJ09NO0000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"
