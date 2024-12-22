from fastapi import FastAPI, Query, Depends
from datetime import date
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as pages_router

app = FastAPI()

app.include_router(router=router_users)
app.include_router(router=router_bookings)
app.include_router(router=router_hotels)
app.include_router(router=rooms_router)
app.include_router(router=pages_router)


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


# @app.get("/hotels")
# def get_hotels(search_args: HotelsSearchArgs = Depends()):
#     return search_args
