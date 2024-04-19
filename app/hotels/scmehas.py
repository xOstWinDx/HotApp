from pydantic import BaseModel


class SHotels(BaseModel):
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
