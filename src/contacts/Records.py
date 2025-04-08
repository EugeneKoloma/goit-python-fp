from colorama import Fore

from .Fields import Birthday, Name, Phone


class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

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
