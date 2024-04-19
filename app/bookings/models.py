from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey(Rooms.id))
    user_id = Column(Integer, ForeignKey(Users.id, ondelete="CASCADE"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer)
    total_days = Column(Integer, Computed(date_to - date_from))
    total_cost = Column(Integer, Computed((date_to - date_from) * price))

    user = relationship("Users", back_populates="booking", cascade="all")
    room = relationship("Rooms", back_populates="booking")

    def __str__(self):
        return f"Booking #{self.id}"
