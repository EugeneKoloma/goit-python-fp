from colorama import Fore

from decorators import error_handler
from exceptions import (
    EmailAlreadyOwned,
    FieldNotFound,
    InvalidDaysInput,
    PhoneAlreadyOwned,
    RecordNotFound,
)
from output import (
    display_birthdays_table,
    display_contacts_table,
    output_info,
    output_warning,
)
from utils.search import elastic_search

from .ContactFields import is_valid_birthday, is_valid_email, is_valid_phone
from .ContactsBook import ContactsBook
from .Records import Record


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
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        birthday = data.get("birthday")
        tags = data.get("tags")

        if self.book.is_phone_owned(phone):
            raise PhoneAlreadyOwned(
                f"This number {Fore.YELLOW}{phone}{Fore.RESET} already owned."
            )

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
        output_info(f"Contact {name} has been added successfully.")

    @error_handler
    def edit_contact_field(
        self, name: str, field: str, new_value: str, old_value: str = ""
    ):
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
                if self.book.is_email_owned(new_value):
                    raise EmailAlreadyOwned(
                        f"This email {Fore.YELLOW}{new_value}{Fore.RESET} already owned."
                    )
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
            case "tag":
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

        output_info(f"Contact {name}'s field '{field}' has been updated.")

    @error_handler
    def remove_contact_field(self, name: str, field: str, value: str):
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(f"Contact {Fore.GREEN}{name}{Fore.RESET} not found.")

        match field:
            case "phone":
                phone = record.find_phone(value)
                if phone:
                    record.phones.remove(phone)
                else:
                    raise FieldNotFound(f"Phone {value} not found.")
            case "email":
                email = record.find_email(value)
                if email:
                    record.emails.remove(email)
                else:
                    raise FieldNotFound(f"Email {value} not found.")
            case "address":
                if record.address:
                    record.address = None
                else:
                    raise FieldNotFound(f"Address {value} not found.")
            case "birthday":
                if record.birthday:
                    record.birthday = None
                else:
                    raise FieldNotFound(f"Birthday {value} not found.")
            case "tag":
                tag = record.find_tag(value)
                if tag:
                    record.tags.remove(tag)
                else:
                    raise FieldNotFound(f"Tag {value} not found.")
            case _:
                raise FieldNotFound(
                    f"Field {Fore.YELLOW}{field}{Fore.RESET} not recognized."
                )

        output_info(f"Contact {name}'s field '{field}' has been removed.")

    @error_handler
    def show_all_contacts(self):
        display_contacts_table(self.book.data.values())

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
                f"Record not found with name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        if record.birthday is None:
            output_warning(f"{name} has not birthday set.")

        output_info(f"{name} has a birthday at: {str(record.birthday)}")

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
        name, old_phone, new_phone = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(f"Record not found for name: {name}")

        phone = record.find_phone(old_phone)
        if phone is None:
            raise FieldNotFound(
                f"Phone number {new_phone} not exist. You can add it using the 'add' command."
            )

        if self.book.is_phone_owned(new_phone):
            raise PhoneAlreadyOwned(f"This number {new_phone} already owned.")

        phone.value = new_phone
        output_info(
            f"Contact {name} has been updated with new phone number {new_phone}."
        )

    @error_handler
    def search_contacts(book, query: str):
        return elastic_search(book.data.values(), query)

    @error_handler
    def contact_exists(self, name: str) -> bool:
        return any(
            str(record.name).lower() == name.lower()
            for record in self.book.data.values()
        )

    @error_handler
    def validate_field(self, field: str, value: str) -> bool:
        if field == "phone":
            return is_valid_phone(value)
        elif field == "email":
            return is_valid_email(value)
        elif field == "birthday":
            return is_valid_birthday(value)
        # Other basic checks
        return bool(value.strip())

    @error_handler
    def get_all_contact_names(self) -> list[str]:
        return [record.name for record in self.book.data.values()]
