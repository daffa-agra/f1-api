from pydantic import BaseModel


class DriverBase(BaseModel):
    driver_number: int
    name: str
    team: str
    nationality: str | None = None
    headshot_url: str | None = None


class DriverResponse(DriverBase):
    driver_id: int

    class Config:
        from_attributes = True
