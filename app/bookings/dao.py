from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select, insert, func, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.logger import logger
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
        try:
            async with async_session_maker() as session:

                booked_rooms = select(Bookings).where(
                    and_(
                        Bookings.room_id == room_id,
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
                ).cte("booked_rooms")

                get_rooms_left = select(Rooms.quantity - func.count(booked_rooms.c.room_id)
                                    ).select_from(Rooms).outerjoin(
                                        booked_rooms, booked_rooms.c.room_id == Rooms.id,
                                    ).where(Rooms.id == room_id).group_by(
                                        Rooms.quantity, booked_rooms.c.room_id
                                    )
                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = insert(Bookings).values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    ).returning(Bookings)

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()

                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"
                extra = {
                    "user_id": user_id,
                    "room_id": room_id,
                    "date_from": date_from,
                    "date_to": date_to,
                }
            logger.error(msg=msg, extra=extra, exc_info=True)
