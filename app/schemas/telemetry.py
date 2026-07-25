from pydantic import BaseModel


class TelemetryBase(BaseModel):
    lap_id: int
    driver_id: int
    session_id: int
    timestamp: float
    speed: float | None = None
    rpm: float | None = None
    gear: int | None = None
    throttle: float | None = None
    brake: float | None = None
    drs: int | None = None
    distance: float | None = None
    source: str = "car_data"


class TelemetryResponse(TelemetryBase):
    telemetry_id: int

    class Config:
        from_attributes = True
