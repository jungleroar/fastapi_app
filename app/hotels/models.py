from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import JSON
from app.database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str | None]
    services: Mapped[dict | None] = mapped_column(JSON)
    rooms_quantity: Mapped[int | None]
    image_id: Mapped[int | None]
