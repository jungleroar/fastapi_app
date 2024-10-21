from fastapi import FastAPI, Query, Depends
from datetime import date
from pydantic import BaseModel


app = FastAPI()



class HotelsSearchArgs:
    def __init__(self,
                date_from: date,
                date_to: date,
                location: str,
                stars: int = Query(None, ge=1, le=5),
                has_spa: bool = None,
                ) -> None:
        self.date_from = date_from
        self.date_to = date_to
        self.location = location
        self.stars = stars
        self.has_spa = has_spa


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get("/hotels")
def get_hotels(search_args: HotelsSearchArgs = Depends()):
    return search_args


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    

@app.post("/bookings")
def add_booking(booking: SBooking):
    pass