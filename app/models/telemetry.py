from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship


class Telemetry(Base):
    __tablename__ = "telemetry"

    telemetry_id = Column(Integer, primary_key=True, autoincrement=True)
    lap_id = Column(Integer, ForeignKey("laps.lap_id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=False)
    timestamp = Column(Float, nullable=False)
    speed = Column(Float, nullable=True)
    rpm = Column(Float, nullable=True)
    gear = Column(Integer, nullable=True)
    throttle = Column(Float, nullable=True)
    brake = Column(Float, nullable=True)
    drs = Column(Integer, nullable=True)
    distance = Column(Float, nullable=True)
    source = Column(String(50), nullable=False, default="car_data")

    lap = relationship("Lap", back_populates="telemetry")
    driver = relationship("Driver", back_populates="telemetry")
    session = relationship("Session", back_populates="telemetry")

    __table_args__ = (
        Index("idx_telemetry_session_driver_ts", "session_id", "driver_id", "timestamp"),
    )
