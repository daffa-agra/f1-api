from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str
    nationality: str | None = None


class TeamResponse(TeamBase):
    team_id: int

    class Config:
        from_attributes = True
