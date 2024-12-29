from fastapi import APIRouter, Query
from app.hotels.dao import HotelsDAO
from datetime import date, datetime
from app.hotels.schemas import SHotel
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as
import asyncio

router = APIRouter(prefix="/hotels",
                   tags=["Отели и номера"])


@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location_and_date(location: str,
                                          date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
                                          date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
                                        ):
    hotels = await HotelsDAO.search_for_hotels(location, date_from, date_to)
    # hotels_json = parse_obj_as(list[SHotel], hotels)
    await asyncio.sleep(3)
    return hotels


@router.get("/all")
async def get_all_hotels():
    return await HotelsDAO.find_all()