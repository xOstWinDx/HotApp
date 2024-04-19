from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_list = [Users.id, Users.email, Users.is_super, Users.booking]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-sharp fa-solid fa-users"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-sharp fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.booking]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-sharp fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [
        Bookings.user,
        Bookings.room,
    ]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-sharp fa-solid fa-book"
