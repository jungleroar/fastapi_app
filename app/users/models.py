from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from app.database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    booking: Mapped["Bookings"] = relationship(back_populates='user')

    def __str__(self):
        return self.email
    