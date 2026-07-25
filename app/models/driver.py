from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship


class Driver(Base):
    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True, autoincrement=True)
    driver_number = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    team = Column(String(255), nullable=False, index=True)
    nationality = Column(String(255), nullable=True)
    headshot_url = Column(String(512), nullable=True)

    laps = relationship("Lap", back_populates="driver")
    telemetry = relationship("Telemetry", back_populates="driver")
    pit_stops = relationship("PitStop", back_populates="driver")
