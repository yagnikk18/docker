from sqlalchemy import Column, String, Float
from app.database import Base

class Vehicle(Base):
    """
    SQLAlchemy ORM model representing a vehicle.

    Each vehicle is uniquely identified by its license plate number
    and has an associated prepaid balance.

    Attributes
    ----------
    plate_number : str
        The unique license plate number of the vehicle (primary key).
    balance : float
        The current prepaid balance associated with the vehicle. Defaults to 0.0.
    """
    __tablename__ = "vehicles"

    plate_number: str = Column(
        String(32), primary_key=True, index=True, nullable=False
    )
    balance: float = Column(Float, default=0.0, nullable=False)

 