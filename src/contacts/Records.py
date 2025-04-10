"""
Command Use Example for tags in contacts:

> add-tag "John Doe" #friend -> call add_tag(tag) method
> show-tags "John Doe" -> call remove_tag(tag) method

"""

from colorama import Fore

from common.tag import Tag

from .ContactFields import Birthday, Name, Phone


class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.tags: list[Tag] = []

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def edit_phone(self, previous_phone, new_phone):
        found_phone = self.find_phone(previous_phone)
        found_phone.value = new_phone

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        self.phones.remove(found_phone)

    def find_phone(self, phone: str) -> Phone | None:
        found_phone = next((item for item in self.phones if item.value == phone), None)
        return found_phone

    # Add tag to contact record
    def add_tag(self, tag: Tag):
        if tag not in self.tags:
            self.tags.append(tag)

    # Remove tag from contact record
    def remove_tag(self, tag: Tag):
        self.tags = [t for t in self.tags if t != tag]

    # Show tags from contact record
    def list_tags(self):
        return [str(tag) for tag in self.tags]

    # Return a list of string-convertible fields for elastic search to function properly
    def get_all_fields(self):
        return [
            str(self.name),
            *[str(phone) for phone in self.phones],
            # *[str(email) for email in self.emails], # Uncomment as soon as we have e-mail field
            str(self.birthday) if self.birthday else "",
            *[str(tag) for tag in self.tags],
        ]

    def __str__(self):
        birthday = (
            f"Birthday: {Fore.MAGENTA}{self.birthday}{Fore.RESET}"
            if self.birthday
            else ""
        )
        return (
            f"Contact name: {Fore.CYAN}{self.name._value.capitalize()}{Fore.RESET}. "
            f"Phones: {Fore.YELLOW}{' '.join(p.value for p in self.phones)}{Fore.RESET} "
            + birthday
        )
