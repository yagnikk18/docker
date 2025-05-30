from sqlalchemy.orm import Session
from . import models, schemas


def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    """
    Create a new vehicle record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        vehicle (schemas.VehicleCreate): Vehicle data from the request payload.

    Returns:
        models.Vehicle: The newly created vehicle object.
    """
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def get_vehicle(db: Session, plate_number: str):
    """
    Retrieve a vehicle by its plate number.

    Args:
        db (Session): SQLAlchemy database session.
        plate_number (str): The vehicle's plate number.

    Returns:
        models.Vehicle | None: The vehicle object if found, otherwise None.
    """
    return db.query(models.Vehicle).filter(models.Vehicle.plate_number == plate_number).first()


def add_balance(db: Session, plate_number: str, amount: float):
    """
    Add balance to an existing vehicle's account.

    Args:
        db (Session): SQLAlchemy database session.
        plate_number (str): The vehicle's plate number.
        amount (float): The amount to add to the vehicle's balance.

    Returns:
        models.Vehicle | None: The updated vehicle object if found, otherwise None.
    """
    vehicle = get_vehicle(db, plate_number)
    if vehicle:
        vehicle.balance += amount
        db.commit()
        db.refresh(vehicle)
    return vehicle
