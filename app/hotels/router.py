from fastapi import APIRouter, Query
from app.hotels.dao import HotelsDAO
from datetime import date, datetime

router = APIRouter(prefix="/hotels",
                   tags=["Отели и номера"])


@router.get("")
async def get_hotels_by_location_and_date(location: str,
                                          date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
                                          date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
                                        ):
    hotels = await HotelsDAO.search_for_hotels(location, date_from, date_to)
    return hotels

@router.get("/all")
async def get_all_hotels():
    return await HotelsDAO.find_all()