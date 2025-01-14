from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as pages_router
from app.images.router import router as images_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from app.database import engine
from app.admin.views import UserAdmin, BookingsAdmin, RoomsAdmin, HotelsAdmin


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router=router_users)
app.include_router(router=router_bookings)
app.include_router(router=router_hotels)
app.include_router(router=rooms_router)
app.include_router(router=pages_router)
app.include_router(router=images_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)
