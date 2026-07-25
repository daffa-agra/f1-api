from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Race(Base):
    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True, autoincrement=True)
    circuit_id = Column(Integer, ForeignKey("circuits.circuit_id"), nullable=False)
    season = Column(Integer, nullable=False, index=True)
    round = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    date = Column(String(255), nullable=True)
    time = Column(String(255), nullable=True)

    circuit = relationship("Circuit", back_populates="races")
    sessions = relationship("Session", back_populates="race")

    __table_args__ = (UniqueConstraint("season", "round", name="uq_race_season_round"),)
