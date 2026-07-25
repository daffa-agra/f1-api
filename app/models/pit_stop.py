from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class PitStop(Base):
    __tablename__ = "pit_stops"

    pit_stop_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"), nullable=False)
    lap = Column(Integer, nullable=False)
    stop_duration = Column(Float, nullable=True)
    time_of_day = Column(Float, nullable=True)

    session = relationship("Session", back_populates="pit_stops")
    driver = relationship("Driver", back_populates="pit_stops")
