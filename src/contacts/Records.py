"""
Command Use Example for tags in contacts:

> add-tag "John Doe" #friend -> call add_tag(tag) method
> show-tags "John Doe" -> call remove_tag(tag) method

"""

from colorama import Fore

from common.Tag import Tag

from .ContactFields import Address, Birthday, Email, Name, Phone, Photo


class Record:
    def __init__(
        self,
        name: Name,
        phones: list[Phone] = None,
        birthday=None,
        tags: list[Tag] = None,
        address=None,
        emails: list[Email] = None,
        photo=None,
    ):
        self.name = Name(name)
        self.phones: list[Phone] = phones if phones is not None else []
        self.birthday: Birthday | None = birthday
        self.tags: list[Tag] = tags if tags is not None else []
        self.address: Address | None = address
        self.emails: list[Email] = emails if emails is not None else []
        self.photo: Photo | None = Photo(photo) if photo else None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_address(self, address: str):
        self.address = Address(address)

    def edit_address(self, address: str):
        if self.address:
            self.address.value = address
        else:
            self.add_address(address)

    def add_photo(self, photo: str):
        self.photo = Photo(photo)

    def edit_photo(self, photo: str):
        if self.photo:
            self.photo = Photo(photo)
        else:
            self.add_photo(photo)

    @property
    def ascii_photo_path(self):
        return self.photo.value if self.photo else None

    def find_email(self, email: str) -> Email | None:
        found_email = next((item for item in self.emails if item.value == email), None)
        return found_email

    def add_email(self, email: str):
        if email in [email.value for email in self.emails]:
            raise ValueError(f"Email {email} already exists.")
        self.emails.append(Email(email))

    def edit_email(self, previous_email: str, new_email: str):
        found_email = self.find_email(previous_email)
        if found_email:
            found_email.value = new_email
        else:
            raise ValueError(f"Email {previous_email} not found.")

    def remove_email(self, email: str):
        found_email = self.find_email(email)
        if found_email:
            self.emails.remove(found_email)
        else:
            raise ValueError(f"Email {email} not found.")

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

    def add_tag(self, tag: Tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: Tag):
        self.tags = [t for t in self.tags if t != tag]

    def list_tags(self):
        return [str(tag) for tag in self.tags]

    def find_tag(self, tag: str) -> Tag | None:
        found_tag = next((item for item in self.tags if item.value == tag), None)
        return found_tag

    # Return a list of string-convertible fields for elastic search to function properly
    def get_all_fields(self):
        return [
            str(self.name),
            *[str(phone) for phone in self.phones],
            *[str(email) for email in self.emails],
            str(self.address) if self.address else "",
            str(self.birthday) if self.birthday else "",
            *[str(tag) for tag in self.tags],
            str(self.photo) if self.photo else "",
        ]

    def get_field_values_list(self, field: str) -> list[str]:
        """
        Returns a string representation of the field's current value,
        or None if the field does not exist or is empty.
        """

        match field:
            case "phone" | "phones":
                return [str(p) for p in self.phones]
            case "email" | "emails":
                return [str(e) for e in self.emails]
            case "tags":
                return [str(t) for t in self.tags]
            case "birthday":
                return [str(self.birthday)] if self.birthday else []
            case "address":
                return [str(self.address)] if self.address else []
            case "name":
                return [str(self.name)] if self.name else []
            case _:
                return []

    def __str__(self):
        birthday = (
            f"Birthday: {Fore.MAGENTA}{self.birthday}{Fore.RESET}."
            if self.birthday
            else ""
        )
        emails = (
            f"Emails: {Fore.YELLOW}{' '.join(e.value for e in self.emails)}{Fore.RESET} "
            if self.emails
            else ""
        )
        address = (
            f"Address: {Fore.YELLOW}{self.address}{Fore.RESET} " if self.address else ""
        )
        tags = (
            f"Tags: {Fore.LIGHTGREEN_EX}{' '.join(str(tag) for tag in self.tags)}{Fore.RESET} "
            if self.tags
            else ""
        )
        # photo = (
        #     f"Photo: {Fore.LIGHTGREEN_EX}{self.photo}{Fore.RESET} "
        #     if self.photo
        #     else ""
        # )
        return (
            f"Contact name: {Fore.CYAN}{self.name._value.capitalize()}{Fore.RESET}. "
            f"Phones: {Fore.YELLOW}{' '.join(p.value for p in self.phones)}{Fore.RESET} "
            f"{emails}{tags}{address}{birthday}"
        )

    def __setstate__(self, state):
        self.__dict__.update(state)
        if "emails" not in state:
            self.emails = []
        if "address" not in state:
            self.address = None
        if "birthday" not in state:
            self.birthday = None
        if "tags" not in state:
            self.tags = []
        if "photo" not in state:
            self.photo = None
