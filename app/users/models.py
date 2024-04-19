from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_super: bool = Column(Boolean)

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"{self.email}"
