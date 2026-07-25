from pydantic import BaseModel


class PitStopBase(BaseModel):
    session_id: int
    driver_id: int
    lap: int
    stop_duration: float | None = None
    time_of_day: float | None = None


class PitStopResponse(PitStopBase):
    pit_stop_id: int

    class Config:
        from_attributes = True
