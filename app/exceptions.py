from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TokenWasExpiredException(BookingException):
    detail = "Токен истёк"
    status_code = status.HTTP_401_UNAUTHORIZED


class UncorrectableTokenException(BookingException):
    detail = "Невалидный токен"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenNoHasUserIDException(BookingException):
    detail = "Неправильный токен"
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotFoundException(BookingException):
    detail = "Не верные данные"
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotIsSuperException(BookingException):
    detail = "У вас нет доступа"
    status_code = status.HTTP_423_LOCKED


class UserAlreadyExistException(BookingException):
    detail = "Пользователь уже зарегистрирован"
    status_code = status.HTTP_409_CONFLICT


class IncorrectEmailOrPassword(BookingException):
    detail = "Не верные Email или Пароль"
    status_code = status.HTTP_401_UNAUTHORIZED


class CantADDBoockingsException(BookingException):
    detail = "Не возможно забронировать"
    status_code = status.HTTP_409_CONFLICT


class CantADDBookingsIncorrectDate(BookingException):
    detail = "Не верная дата"
    status_code = status.HTTP_400_BAD_REQUEST
