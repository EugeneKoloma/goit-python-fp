from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator

from contacts.validators import (
    BirthdayValidator,
    EmailValidator,
    NameValidator,
    PhoneValidator,
    TagsValidator,
)
from output import output_error

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


# Get enew contact details for autofill purposes to avoid name field autofill
def get_new_contact_details(book):
    name = ask_field(
        "Name", validator=NameValidator(book)
    )  # validator should ensure uniqueness!
    phone = ask_field("Phone", validator=PhoneValidator(book))
    email = ask_field(
        "Email (optional)", validator=EmailValidator(book), required=False
    )
    address = ask_field("Address (optional)", required=False)
    birthday = ask_field(
        "Birthday (optional, DD.MM.YYYY)", validator=BirthdayValidator(), required=False
    )
    tags_input = ask_field(
        "Tags (optional, comma-separated)", validator=TagsValidator(), required=False
    )

    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

    return {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "birthday": birthday,
        "tags": tags,
    }


# Get existing contact details for autofill purposes
def get_existing_contact_details(book):
    name_completer = get_name_completer(book)

    name = ask_field("Name", completer=name_completer)
    phone = ask_field("Phone", validator=PhoneValidator(book))
    email = ask_field(
        "Email (optional)", validator=EmailValidator(book), required=False
    )
    address = ask_field("Address (optional)", required=False)
    birthday = ask_field(
        "Birthday (optional, DD.MM.YYYY)", validator=BirthdayValidator(), required=False
    )
    tags_input = ask_field(
        "Tags (optional, comma-separated)", validator=TagsValidator(), required=False
    )

    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

    return {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "birthday": birthday,
        "tags": tags,
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


def get_name_completer(book):
    return WordCompleter(list(book.data.keys()), ignore_case=True)


def ask_field(label, validator=None, required=True, completer=None):
    while True:
        try:
            value = prompt(f"{label}: ", completer=completer, validator=validator)
        except Exception as e:
            output_error(str(e))
            continue

        if not value and not required:
            return ""
        return value
