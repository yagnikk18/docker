"""
vehicle_api.py

A minimal FastAPI service that lets clients register a vehicle,
top-up its prepaid balance, and query the current balance.

Endpoints
---------
POST /register
    Register a new vehicle.

POST /topup/{plate_number}
    Add funds to an existing vehicle’s balance.

GET /balance/{plate_number}
    Retrieve the full vehicle record (including current balance).
"""

from typing import Generator

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from app import models, schemas, crud, database

#: FastAPI application instance
app = FastAPI()

# ---------------------------------------------------------------------------#
# Database plumbing
# ---------------------------------------------------------------------------#

# Ensure tables exist at startup. In production, you might run migrations
# (Alembic) instead of automating this in code.
models.Base.metadata.create_all(bind=database.engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and guarantee it’s closed afterwards.

    Yields
    ------
    Session
        An SQLAlchemy session tied to the request lifetime.
    """
    db: Session = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------#
# API routes
# ---------------------------------------------------------------------------#

@app.post(
    "/register",
    response_model=schemas.Vehicle,
    status_code=201,
    summary="Register a vehicle",
    description="Create a new vehicle record. The `plate_number` must be unique.",
)
def register_vehicle(
    vehicle: schemas.VehicleCreate,
    db: Session = Depends(get_db),
) -> schemas.Vehicle:
    """Create a new vehicle record.

    Parameters
    ----------
    vehicle : schemas.VehicleCreate
        Request body containing plate number and initial balance.
    db : Session, optional
        SQLAlchemy session injected by FastAPI’s DI.

    Returns
    -------
    schemas.Vehicle
        The newly created vehicle record.

    Raises
    ------
    HTTPException (400)
        If a vehicle with the same plate number already exists.
    """
    if crud.get_vehicle(db, vehicle.plate_number):
        raise HTTPException(status_code=400, detail="Vehicle already registered")
    return crud.create_vehicle(db, vehicle)


@app.post(
    "/topup/{plate_number}",
    response_model=schemas.Vehicle,
    summary="Top-up balance",
    description="Add funds to an existing vehicle’s balance.",
)
def top_up_balance(
    plate_number: str,
    topup: schemas.VehicleUpdate,
    db: Session = Depends(get_db),
) -> schemas.Vehicle:
    """Add balance to a vehicle’s prepaid account.

    Parameters
    ----------
    plate_number : str
        Vehicle’s unique license plate number.
    topup : schemas.VehicleUpdate
        Payload containing the `amount` to add.
    db : Session, optional
        SQLAlchemy session injected by FastAPI.

    Returns
    -------
    schemas.Vehicle
        The updated vehicle record with the new balance.

    Raises
    ------
    HTTPException (404)
        If the vehicle is not found.
    """
    vehicle = crud.add_balance(db, plate_number, topup.amount)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@app.get(
    "/balance/{plate_number}",
    response_model=schemas.Vehicle,
    summary="Get balance",
    description="Retrieve the current balance (and other info) for a vehicle.",
)
def get_balance(
    plate_number: str,
    db: Session = Depends(get_db),
) -> schemas.Vehicle:
    """Fetch the vehicle record for the given plate number.

    Parameters
    ----------
    plate_number : str
        Vehicle’s unique license plate number.
    db : Session, optional
        SQLAlchemy session injected by FastAPI.

    Returns
    -------
    schemas.Vehicle
        Vehicle record if found.

    Raises
    ------
    HTTPException (404)
        If the vehicle is not found.
    """
    vehicle = crud.get_vehicle(db, plate_number)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
