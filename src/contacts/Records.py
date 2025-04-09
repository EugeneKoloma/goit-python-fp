from colorama import Fore

from .ContactFields import Birthday, Email, Name, Phone


class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.emails: list[Email] = []

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def edit_phone(self, previous_phone, new_phone):
        found_phone = self.find_phone(previous_phone)
        found_phone.value = new_phone  # type: ignore

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        self.phones.remove(found_phone)  # type: ignore

    def find_phone(self, phone: str) -> Phone | None:
        found_phone = next((item for item in self.phones if item.value == phone), None)
        return found_phone

    # ====================================MAIL====================================
    def add_email(self, email: str):
        self.emails.append(Email(email))

    def edit_email(self, old_email: str, new_email: str):
        found_email = self.find_email(old_email)
        if found_email:
            found_email.value = new_email

    def remove_email(self, email_str: str):
        found_email = self.find_email(email_str)
        if found_email is not None:
            self.emails.remove(found_email)

    def find_email(self, email_str: str) -> Email | None:
        return next((e for e in self.emails if e.value == email_str), None)

    # ====================================MAIL=====================================
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
