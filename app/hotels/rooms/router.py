from app.hotels.router import router
from app.hotels.rooms.dao import RoomsDAO
from app.hawk import hawk


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    return await RoomsDAO.find_all(hotel_id=hotel_id)
