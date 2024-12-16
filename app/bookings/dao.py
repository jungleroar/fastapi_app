from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select, func, and_, or_
from app.bookings.models import Bookings
from app.rooms.models import Rooms
from datetime import date

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date,
                  ):
        async with async_session_maker() as session:

            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        ), 
                    )
                )
            )

            rooms_left = select(Rooms.quantity - func.count(booked_rooms.c.room_id)
                                ).select_from(Rooms).join(
                                    booked_rooms, booked_rooms.c.room_id == Rooms.id
                                ).where(Rooms.id == 1).group_by(
                                    Rooms.quantity, booked_rooms.c.room_id
                                )
            