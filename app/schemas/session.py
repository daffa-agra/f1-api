from pydantic import BaseModel


class SessionBase(BaseModel):
    race_id: int
    session_type: str
    date: str | None = None
    time: str | None = None


class SessionResponse(SessionBase):
    session_id: int

    class Config:
        from_attributes = True
