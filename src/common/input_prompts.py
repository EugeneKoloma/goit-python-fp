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


# Validate tags
class TagsValidator(Validator):
    def validate(self, document):
        if document.text:
            tags = [tag.strip() for tag in document.text.split(",")]
            for tag in tags:
                if not tag.startswith("#") or not tag[1:].isalnum():
                    raise ValidationError(
                        message="Each tag must start with '#' and contain only letters or digits (e.g., #Work, #Family)."
                    )


field_value_completers = {
    "phone": WordCompleter(
        [], ignore_case=True
    ),  # can fill with contact phones if needed
    "email": WordCompleter([], ignore_case=True),
    "address": WordCompleter([], ignore_case=True),
    "birthday": WordCompleter([], ignore_case=True),
    "tags": WordCompleter([], ignore_case=True),
    # Extend with known values or logic later
}


# Get supported fields for long add command
def get_supported_fields():
    return list(field_value_completers.keys())


# Valitate fields for long add command
def is_valid_field(field: str) -> bool:
    return field in field_value_completers


# Autofill for fields for long add command
def prompt_for_field(field: str) -> str:
    completer = field_value_completers.get(field)
    return prompt(f"Enter value for {field}: ", completer=completer)


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
    tags_input = prompt("Tags (optional, comma-separated): ", validator=TagsValidator())
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

    return {
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip() or None,
        "address": address.strip() or None,
        "birthday": birthday.strip() or None,
        "tags": tags or None,
    }


# Edit contact with fields selection
def edit_contact_prompt(book):
    names = list(book.data.keys())
    name_completer = WordCompleter(names, ignore_case=True)
    name = prompt("Which contact do you want to edit? ", completer=name_completer)

    field_options = ["name", "phone", "email", "address", "birthday", "tags"]
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
        case "tags":
            return TagsValidator()
        case _:
            return Validator.from_callable(lambda t: True)  # no validation


def prompt_missing_args(
    required_fields: list[str], provided_args: dict[str, str]
) -> dict[str, str]:
    """
    Prompts for any missing required fields using prompt_toolkit.

    Args:
        required_fields: A list of required field names.
        provided_args: A dict of already provided args.

    Returns:
        A full dict with all required fields filled.
    """
    result = provided_args.copy()
    for field in required_fields:
        if field not in result or not result[field]:
            result[field] = prompt(f"Enter {field}: ")
    return result
