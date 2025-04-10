import re
from datetime import datetime

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import ValidationError, Validator


# Validate phone
class PhoneValidator(Validator):
    def validate(self, document):
        if not document.text.isdigit():
            raise ValidationError(message="Phone must contain digits only.")


# Validate email
class EmailValidator(Validator):
    def validate(self, document):
        if document.text and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", document.text):
            raise ValidationError(message="Invalid email format.")


# Validate birthday
class BirthdayValidator(Validator):
    def validate(self, document):
        if document.text:
            try:
                datetime.strptime(document.text, "%d.%m.%Y")
            except ValueError:
                raise ValidationError(message="Date must be in DD.MM.YYYY format.")


# Get contact details for autofill purposes
def get_contact_details():
    name = prompt(
        "Name: ",
        validator=Validator.from_callable(
            lambda t: len(t.strip()) > 0,
            error_message="Name cannot be empty.",
            move_cursor_to_end=True,
        ),
    )

    phone = prompt("Phone: ", validator=PhoneValidator())
    email = prompt("Email (optional): ", validator=EmailValidator())
    address = prompt("Address (optional): ")
    birthday = prompt(
        "Birthday (optional, DD.MM.YYYY): ", validator=BirthdayValidator()
    )

    return {
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip() or None,
        "address": address.strip() or None,
        "birthday": birthday.strip() or None,
    }


# Edit contact with fields selection
def edit_contact_prompt(book):
    names = list(book.data.keys())
    name_completer = WordCompleter(names, ignore_case=True)
    name = prompt("Which contact do you want to edit? ", completer=name_completer)

    field_options = ["name", "phone", "email", "address", "birthday"]
    field_completer = WordCompleter(field_options, ignore_case=True)
    field = prompt("Which field do you want to edit? ", completer=field_completer)

    record = book.find(name)
    if not record:
        print(f"Contact '{name}' not found.")
        return None, None, None

    current_value = getattr(record, field, None)
    if callable(current_value):
        current_value = current_value()

    print(f"Current value for {field}: {current_value}")

    new_value = prompt("New value: ", validator=get_field_validator(field))
    return name, field, new_value.strip()


# Get fields selection with validation
def get_field_validator(field):
    match field:
        case "phone":
            return PhoneValidator()
        case "email":
            return EmailValidator()
        case "birthday":
            return BirthdayValidator()
        case _:
            return Validator.from_callable(lambda t: True)  # no validation
