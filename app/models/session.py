from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey("races.race_id"), nullable=False)
    session_type = Column(String(50), nullable=False)
    date = Column(String(255), nullable=True)
    time = Column(String(255), nullable=True)

    race = relationship("Race", back_populates="sessions")
    laps = relationship("Lap", back_populates="session")
    telemetry = relationship("Telemetry", back_populates="session")
    pit_stops = relationship("PitStop", back_populates="session")

    __table_args__ = (UniqueConstraint("race_id", "session_type", name="uq_session_race_type"),)
