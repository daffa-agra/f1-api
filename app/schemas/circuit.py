from pydantic import BaseModel


class CircuitBase(BaseModel):
    circuit_key: int
    name: str
    location: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class CircuitResponse(CircuitBase):
    circuit_id: int

    class Config:
        from_attributes = True
