import os
import re
from datetime import datetime as dt

from common import Field
from exceptions import WrongDateFormat, WrongEmailValue, WrongPhoneNumber


class Name(Field):
    pass


class Phone(Field):
    __phone_pattern = re.compile(r"^\+?3?8?(0\d{9})$|^0\d{9}$")

    @staticmethod
    def validate_phone_number(phone_number):
        return bool(Phone.__phone_pattern.match(phone_number))

    def __init__(self, phone: str):
        self.value = phone

    def __str__(self):
        return self._value or ""

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
        try:
            dt.strptime(date, Birthday.date_format_pattern)
            return (True) and (
                dt.strptime(date, Birthday.date_format_pattern) < dt.now()
            )
        except ValueError:
            return False

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


class Address(Field):
    def __init__(self, address: str):
        self.value = address

    def __str__(self):
        return self._value or ""

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, address: str):
        if not address or not isinstance(address, str):
            self._value = None
            return

        self._value = address

    def __eq__(self, other):
        if isinstance(other, Address):
            return self.value == other.value
        return False


class Email(Field):
    __email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def __str__(self):
        return self._value or ""

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(Email.__email_pattern.match(email))

    def __init__(self, email: str):
        self.value = email

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, email: str):
        if not Email.validate_email(email):
            raise WrongEmailValue(f"Wrong email format {email}.")
        self._value = email

    def __eq__(self, other):
        if isinstance(other, Email):
            return self.value == other.value
        return False


class Photo(Field):
    def __init__(self, path: str):
        self.value = path

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, path: str):
        if (
            path
            and isinstance(path, str)
            and path.endswith(".txt")
            and os.path.isfile(path)
        ):
            self._value = path
        else:
            self._value = None  # or raise an error

    def __str__(self):
        return self._value or "[No Photo]"

    @staticmethod
    def validate_path(path: str) -> bool:
        """Validate that the path is a .txt file and exists."""
        return bool(
            path and isinstance(path, str) and path.endswith(".txt")
        )  # and os.path.isfile(path))
