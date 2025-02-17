from fastapi import APIRouter, Query
from app.hotels.dao import HotelDAO
from datetime import date, datetime
from app.hotels.schemas import SHotel
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as
import asyncio
from app.hawk import hawk

router = APIRouter(prefix="/hotels",
                   tags=["Отели и номера"])


@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location_and_date(location: str,
                                          date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
                                          date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
                                        ):
    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)
    # hotels_json = parse_obj_as(list[SHotel], hotels)
    await asyncio.sleep(3)
    return hotels


@router.get("/all")
async def get_all_hotels():
    return await HotelDAO.find_all()


@router.get("/id/{hotel_id}", include_in_schema=True)
# Этот эндпоинт используется для фронтенда, когда мы хотим отобразить все
# номера в отеле и информацию о самом отеле. Этот эндпоинт как раз отвечает за информацию
# об отеле.
# В нем нарушается правило именования эндпоинтов: конечно же, /id/ здесь избыточен.
# Тем не менее, он используется, так как эндпоинтом ранее мы уже задали получение
# отелей по их локации вместо id.
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    return await HotelDAO.find_one_or_none(id=hotel_id)
