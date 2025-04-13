import re

from colorama import Fore
from rapidfuzz import fuzz

from contacts import Birthday, Email, Phone
from decorators import error_handler
from exceptions import (
    FieldNotFound,
    InvalidDaysInput,
    PhoneAlreadyOwned,
    RecordNotFound,
)
from output import (
    default_contacts_table_fields,
    display_birthdays_table,
    display_contacts_table,
    output_info,
    output_warning,
)
from utils.search import elastic_search

from .ContactsBook import ContactsBook
from .Records import Record
from .undo import save_undo_state
from utils.export_import import (
    export_contacts_to_csv,
    import_contacts_to_csv
)


class PhoneBookService:
    def __init__(self, book: ContactsBook):
        self.__book: ContactsBook = book

    @property
    def book(self):
        return self.__book

    @book.setter
    def book(self, book: ContactsBook):
        self.book = book

    @error_handler
    def add_contact_from_dict(self, data: dict):
        save_undo_state(self.book)
        global UNDONE
        UNDONE = False

        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        birthday = data.get("birthday")
        tags = data.get("tags")

        new_record = Record(name)
        new_record.add_phone(phone)

        if email:
            new_record.add_email(email)
        if address:
            new_record.add_address(address)
        if birthday:
            new_record.add_birthday(birthday)
        if tags:
            for tag in tags:
                new_record.add_tag(tag)

        self.book.add_record(new_record)
        # output_info(f"Contact {name} has been added successfully.")

    @error_handler
    def edit_contact_field(
        self, name: str, field: str, new_value: str, old_value: str = ""
    ):
        save_undo_state(self.book)
        global UNDONE
        UNDONE = True

        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(f"Contact {Fore.GREEN}{name}{Fore.RESET} not found.")

        match field:
            case "name":
                record.name._value = new_value
            case "phone":
                if self.book.is_phone_owned(new_value):
                    raise PhoneAlreadyOwned(
                        f"This number {Fore.YELLOW}{new_value}{Fore.RESET} already owned."
                    )
                if record.phones:
                    record.add_phone(new_value)
                else:
                    record.add_phone(new_value)
            case "email":
                if not old_value:
                    record.add_email(new_value)
                    return
                old_email = record.find_email(old_value)
                if old_email:
                    old_email.value = new_value
                    print(f"Email {old_value} has been updated to {new_value}.")
                else:
                    raise FieldNotFound(f"Email {old_value} not found.")
            case "address":
                record.add_address(new_value)
            case "birthday":
                record.add_birthday(new_value)

            case "tags":
                if not old_value:
                    record.add_tag(new_value)
                    return

                tag = record.find_tag(old_value)
                if tag:
                    tag.value = new_value
                    print(f"Tag {old_value} has been updated to {new_value}.")
                else:
                    raise FieldNotFound(f"Tag {old_value} not found.")
            case _:
                raise FieldNotFound(
                    f"Field {Fore.YELLOW}{field}{Fore.RESET} not recognized."
                )

        # output_info(f"Contact {name}'s field '{field}' has been updated.")

    @error_handler
    def show_all_contacts(self, args: list[str] = []) -> None:
        if args:
            final_collumns = ["Name"]
            unknown_fields = ""
            for arg in args:
                if (
                    arg.capitalize() in default_contacts_table_fields
                    and arg.capitalize() not in final_collumns
                ):
                    final_collumns.append(arg.capitalize())
                else:
                    unknown_fields += f"{arg.capitalize()}, "
            if unknown_fields:
                output_info(
                    f"There are no {unknown_fields[:-2]} among ContactsBook fields!"
                )
            display_contacts_table(self.book.data.values(), final_collumns)
        else:
            display_contacts_table(self.book.data.values())

    @error_handler
    def show_sorted_contacts(self, sorted: ContactsBook) -> None:
        self.sorted = sorted
        display_contacts_table(self.sorted)

    @error_handler
    def show_next_n_days_birthdays(self, args: list):
        try:
            days_to = int(args[0].strip(" ,")) if args else 7
        except ValueError:
            raise InvalidDaysInput(f"Wrong days input: {args[0]}")

        congrats_list = self.book.find_next_n_days_bithdays(days_to)
        if congrats_list:
            display_birthdays_table(congrats_list, days_to)
        else:
            output_info(f"No birthdays in the next {days_to} days.")

    @error_handler
    def show_contacts_phones(self, args):
        name = args[0]
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found with name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        display_contacts_table([record])

    @error_handler
    def get_birthday(self, args):
        name = args[0]
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found with name: {Fore.GREEN}{name.capitalize()}{Fore.RESET}"
            )

        if record.birthday is None:
            output_warning(f"{name.capitalize()} has not birthday set.")

        output_info(f"{name.capitalize()} has a birthday at: {str(record.birthday)}")

    @error_handler
    def set_birthday(self, args):
        name, date = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(f"Record not found with name: {name}")

        record.add_birthday(date)
        output_info(f"Contact's {name} birthday was updated: {date}.")

    @error_handler
    def change_contacts_phone(self, args) -> None:
        save_undo_state(self.book)
        global UNDONE
        UNDONE = True

        name, old_phone, new_phone = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(f"Record not found for name: {name}")

        phone = record.find_phone(old_phone)
        if phone is None:
            raise FieldNotFound(
                f"Phone number {new_phone} not exist. You can add it using the 'add' command."
            )

        phone.value = new_phone
        output_info(
            f"Contact {name} has been updated with new phone number {new_phone}."
        )

    @error_handler
    def search_contacts(self, query: str):
        return elastic_search(self.book.data.values(), query)

    @error_handler
    def contact_exists(self, name: str) -> bool:
        return any(
            str(record.name).lower() == name.lower()
            for record in self.book.data.values()
        )

    @error_handler
    def validate_field(self, field: str, value: str) -> bool:
        validators = {
            "phone": Phone.validate_phone_number,
            "email": Email.validate_email,
            "birthday": Birthday.validate_date,
        }

        validator = validators.get(field)
        if validator:
            return validator(value)

        # Fallback for simple fields like name, address, tag etc.
        return bool(value.strip())

    @error_handler
    def get_all_contact_names(self) -> list[str]:
        return [record.name for record in self.book.data.values()]

    @error_handler
    def find_contacts(self, query: str = "", mode="smart", **filters) -> list:
        results = []

        for record in self.book.data.values():
            # 1. Apply field-specific filters first
            if "name" in filters:
                if filters["name"].lower() not in str(record.name).lower():
                    continue

            if "email" in filters:
                if not any(
                    filters["email"].lower() in str(e).lower()
                    for e in getattr(record, "emails", [])
                ):
                    continue

            if "tag" in filters:
                if not any(
                    filters["tag"].lower() in str(t).lower()
                    for t in getattr(record, "tags", [])
                ):
                    continue

            if "phone" in filters:
                if not any(
                    filters["phone"].lower() in str(p).lower() for p in record.phones
                ):
                    continue

            # 2. Fallback: apply fuzzy or regex search if query is provided
            if query:
                parts = [
                    str(record.name),
                    *[str(p) for p in getattr(record, "phones", [])],
                    *[str(e) for e in getattr(record, "emails", [])],
                    str(getattr(record, "birthday", "")) or "",
                    str(getattr(record, "address", "")) or "",
                    " ".join(str(t) for t in getattr(record, "tags", [])),
                ]
                full_text = " ".join(parts).lower()

                if mode == "regex":
                    try:
                        if not re.search(query, full_text, re.IGNORECASE):
                            continue
                    except re.error:
                        continue  # Skip if regex error

                elif mode == "fuzzy":
                    if fuzz.partial_ratio(query.lower(), full_text) <= 75:
                        continue

                else:  # smart
                    try:
                        if not re.search(query, full_text, re.IGNORECASE):
                            if fuzz.partial_ratio(query.lower(), full_text) <= 75:
                                continue
                    except re.error:
                        if fuzz.partial_ratio(query.lower(), full_text) <= 75:
                            continue

            results.append(record)

        return results

    @error_handler
    def remove_contact_field(self, name: str, field: str, value: str) -> bool:
        save_undo_state(self.book)
        global UNDONE
        UNDONE = True

        record = self.book.find(name)
        if not record:
            return False

        match field:
            case "phone":
                initial_len = len(record.phones)
                record.phones = [p for p in record.phones if str(p) != value]
                return len(record.phones) < initial_len

            case "email":
                initial_len = len(getattr(record, "emails", []))
                record.emails = [
                    e for e in getattr(record, "emails", []) if str(e) != value
                ]
                return len(record.emails) < initial_len

            case "tag":
                initial_len = len(getattr(record, "tags", []))
                record.tags = [
                    t for t in getattr(record, "tags", []) if str(t) != value
                ]
                return len(record.tags) < initial_len

            case _:
                return False

    @error_handler
    def remove_contact(self, name: str | None) -> bool:
        save_undo_state(self.book)
        global UNDONE
        UNDONE = True

        record = self.book.find(name)
        if not record:
            return False

        # Find the actual key that was used to store this contact
        for key, rec in self.book.data.items():
            if rec is record:
                del self.book.data[key]
                return True

        return False

    
    def export_contacts_to_csv(self, args: list[str]):
        if args:
            export_contacts_to_csv(self.book, args)
        else:
            export_contacts_to_csv(self.book)

    def import_contacts_to_csv(self, args: list[str]):
        if args:
            import_contacts_to_csv(self.book, args)
        else:
            import_contacts_to_csv(self.book)