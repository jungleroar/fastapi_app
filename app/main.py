from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as pages_router
from app.images.router import router as images_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router=router_users)
app.include_router(router=router_bookings)
app.include_router(router=router_hotels)
app.include_router(router=rooms_router)
app.include_router(router=pages_router)
app.include_router(router=images_router)
