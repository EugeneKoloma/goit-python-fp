import re
from datetime import datetime as dt

from common import Field
from exceptions import WrongDateFormat, WrongPhoneNumber


class Name(Field):
    pass


class Phone(Field):
    __phone_pattern = re.compile(r"^\+?3?8?(0\d{9})$|^0\d{9}$")

    @staticmethod
    def validate_phone_number(phone_number):
        return bool(Phone.__phone_pattern.match(phone_number))

    def __init__(self, phone: str):
        self.value = phone

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_phone):
        if not Phone.validate_phone_number(new_phone):
            raise WrongPhoneNumber(f"Wrong phone number {new_phone}.")
        self._value = new_phone


class Birthday(Field):
    date_format_pattern = r"%d.%m.%Y"

    @staticmethod
    def validate_date(date: str) -> bool:
        is_datetime = dt.strptime(date, Birthday.date_format_pattern)
        return bool(is_datetime)

    def __init__(self, date: str):
        self.value = date

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, date: str):
        if not Birthday.validate_date(date):
            raise WrongDateFormat(f"Wrong date format {date}")
        self._value = date
