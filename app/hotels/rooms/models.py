from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import JSON
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import Computed
from app.database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[dict | None] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int | None]

    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    booking: Mapped["Bookings"] = relationship(back_populates="room")

    def __str__(self):
        return self.name
