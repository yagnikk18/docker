from pydantic import BaseModel

class VehicleBase(BaseModel):
    """
    Shared base schema for vehicle data.

    Attributes
    ----------
    plate_number : str
        The unique license plate number of the vehicle.
    """
    plate_number: str


class VehicleCreate(VehicleBase):
    """
    Schema for creating a new vehicle.

    Inherits plate number from VehicleBase and adds a starting balance.

    Attributes
    ----------
    balance : float
        The initial balance to set when registering the vehicle.
    """
    balance: float


class VehicleUpdate(BaseModel):
    """
    Schema for topping up a vehicle’s balance.

    Attributes
    ----------
    amount : float
        The amount to add to the vehicle’s current balance.
    """
    amount: float


class Vehicle(VehicleBase):
    """
    Schema for returning vehicle information.

    Extends VehicleBase to include current balance and enables ORM mode
    for integration with SQLAlchemy models.

    Attributes
    ----------
    balance : float
        The current prepaid balance of the vehicle.
    """
    balance: float

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy ORM objects
