from pydantic import BaseModel


class RaceBase(BaseModel):
    season: int
    round: int
    name: str
    date: str | None = None
    time: str | None = None


class RaceResponse(RaceBase):
    race_id: int
    circuit_id: int

    class Config:
        from_attributes = True
