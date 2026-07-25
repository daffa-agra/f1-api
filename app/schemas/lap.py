from pydantic import BaseModel


class LapBase(BaseModel):
    session_id: int
    driver_id: int
    lap_number: int
    lap_time: float | None = None
    sector1_time: float | None = None
    sector2_time: float | None = None
    sector3_time: float | None = None
    tyre_compound: str | None = None
    tyre_age: int | None = None
    weather: str | None = None


class LapResponse(LapBase):
    lap_id: int

    class Config:
        from_attributes = True
