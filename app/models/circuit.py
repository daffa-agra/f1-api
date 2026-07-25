from app.database import Base
from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import relationship


class Circuit(Base):
    __tablename__ = "circuits"

    circuit_id = Column(Integer, primary_key=True, autoincrement=True)
    circuit_key = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    races = relationship("Race", back_populates="circuit")
