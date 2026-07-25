from app.database import Base
from sqlalchemy import Column, Integer, String, Index


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    nationality = Column(String(255), nullable=True)
