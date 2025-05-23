import os
import re
from datetime import datetime as dt

from prompt_toolkit.validation import ValidationError, Validator


class NameValidator(Validator):
    def __init__(self, book):
        self.book = book

    def validate(self, document):
        name = document.text.strip()
        if not name:
            raise ValidationError(message="Name cannot be empty.")
        if name.lower() in (k.lower() for k in self.book.data.keys()):
            raise ValidationError(message=f"Contact '{name}' already exists.")


class PhoneValidator(Validator):
    def __init__(self, book=None):
        self.book = book

    def validate(self, document):
        phone = document.text.strip()

        if not phone.isdigit():
            raise ValidationError(message="Phone must contain digits only.")
        if not is_valid_phone(phone):
            raise ValidationError(message="Invalid phone number format.")

        if self.book:
            for record in self.book.data.values():
                if any(
                    normalize_phone(p.value) == normalize_phone(phone)
                    for p in record.phones
                ):
                    raise ValidationError(
                        message=f"Phone number '{phone}' already exists."
                    )


class EmailValidator(Validator):
    def __init__(self, book=None):
        self.book = book

    def validate(self, document):
        email = document.text.strip()
        if email and not is_valid_email(email):
            raise ValidationError(message="Invalid email format.")
        if self.book and email:
            for record in self.book.data.values():
                if any(e.value == email for e in getattr(record, "emails", [])):
                    raise ValidationError(message=f"Email '{email}' already exists.")


class BirthdayValidator(Validator):
    def validate(self, document):
        if document.text:
            try:
                dt.strptime(document.text, "%d.%m.%Y")
            except ValueError:
                raise ValidationError(message="Date must be in DD.MM.YYYY format.")


class TagsValidator(Validator):
    def validate(self, document):
        if document.text:
            tags = [tag.strip() for tag in document.text.split(",")]
            for tag in tags:
                if not tag[1:].isalnum():
                    raise ValidationError(
                        message="Each tag must contain only letters or digits (e.g., #Work, #Family)."
                    )


class PathValidator(Validator):
    def validate(self, document):
        text = document.text.strip()

        if text == "":
            return

        if not text.endswith(".txt"):
            raise ValidationError(
                message="File must be a .txt file.", cursor_position=len(text)
            )

        if not os.path.isfile(text):
            raise ValidationError(
                message="File does not exist.", cursor_position=len(text)
            )


# Local phone validation to avoid circular import problem
def is_valid_phone(phone: str) -> bool:
    phone_pattern = re.compile(r"^\+?3?8?(0\d{9})$|^0\d{9}$")
    return phone.isdigit() and (bool(phone_pattern.match(phone)))


# Local email validation to avoid circular import problem
def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


# Normalize phone for the search and other needs
def normalize_phone(p: str) -> str:
    """Remove spaces, +38, and keep only digits"""
    return re.sub(r"\D", "", p)[-10:]  # Keep last 9 digits (like 0671234567)
