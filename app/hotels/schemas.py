from pydantic import BaseModel
from datetime import date


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: dict
    rooms_quantity: int
    image_id: int
    
    class Config:
        orm_mode = True