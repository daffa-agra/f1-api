from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Lap(Base):
    __tablename__ = "laps"

    lap_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"), nullable=False)
    lap_number = Column(Integer, nullable=False)
    lap_time = Column(Float, nullable=True)
    sector1_time = Column(Float, nullable=True)
    sector2_time = Column(Float, nullable=True)
    sector3_time = Column(Float, nullable=True)
    tyre_compound = Column(String(50), nullable=True)
    tyre_age = Column(Integer, nullable=True)
    weather = Column(String(255), nullable=True)

    session = relationship("Session", back_populates="laps")
    driver = relationship("Driver", back_populates="laps")
    telemetry = relationship("Telemetry", back_populates="lap")
