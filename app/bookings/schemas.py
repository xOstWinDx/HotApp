from datetime import date

from pydantic import BaseModel, ConfigDict


class SBoockings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int

    model_config = ConfigDict(from_attributes=True)


class SBoockingsWithOtherInfo(SBoockings):
    image_id: int
    name: str
    description: str
    services: list
