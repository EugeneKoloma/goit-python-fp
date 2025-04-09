from colorama import Fore

from decorators import error_handler
from exceptions import FieldNotFound, PhoneAlreadyOwned, RecordNotFound
from output import output_info, output_warning

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
    def add_contact(self, args: list[str]):
        name, phone = args
        record = self.book.find(name)
        if record is None:
            if self.book.is_phone_owned(phone):
                raise PhoneAlreadyOwned(
                    f"This number {Fore.YELLOW}{phone}{Fore.RESET} already owned."
                )

            new_record = Record(name)
            new_record.add_phone(phone)
            self.book.add_record(new_record)
            output_info(
                f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} with phone number {Fore.GREEN}{phone}{Fore.RESET} has been added."
            )
            return

        existing_phone = record.find_phone(phone)
        if existing_phone is None:
            record.add_phone(phone)
            output_info(
                f"New phone number {Fore.GREEN}{phone}{Fore.RESET} was added to {Fore.GREEN}{name.capitalize()}{Fore.RESET}."
            )
            return

        output_warning(
            f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} already has this number {Fore.GREEN}{phone}{Fore.RESET}"
        )

    @error_handler
    def change_contacts_phone(self, args) -> None:
        name, old_phone, new_phone = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found for name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        phone = record.find_phone(old_phone)
        if phone is None:
            raise FieldNotFound(
                f"Phone number {Fore.GREEN}{new_phone}{Fore.RESET} not exist. "\
                f"U can add it by using [{Fore.CYAN}add{Fore.RESET}] command, type help for more info."
            )

        if self.book.is_phone_owned(new_phone):
            raise PhoneAlreadyOwned(
                f"This number {Fore.YELLOW}{new_phone}{Fore.RESET} already owned."
            )

        phone.value = new_phone
        output_info(
            f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} has been updated with new phone number {Fore.GREEN}{phone}{Fore.RESET}."
        )

    @error_handler
    def show_contacts_phones(self, args):
        name = args[0]
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found with name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        print(self.book)

    @error_handler
    def set_birthday(self, args):
        name, date = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found with name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        record.add_birthday(date)
        output_info(
            f"Contact's {Fore.GREEN}{name.capitalize()}{Fore.RESET} birthday was updated: {Fore.GREEN}{date}{Fore.RESET}."
        )

    @error_handler
    def get_birthday(self, args):
        name = args[0]
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found with name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        if record.birthday is None:
            output_warning(
                f"{Fore.GREEN}{name.capitalize()}{Fore.RESET} has not birthday setted."
            )

        output_info(
            f"{Fore.GREEN}{name.capitalize()}{Fore.RESET} has a birthday at: {Fore.GREEN}{str(record.birthday)}{Fore.RESET}"
        )

    @error_handler
    def show_next_week_birthdays(self, args: list):
        '''
        Команда формавання таблиці із списком іменинників на найближчі days_to дні
        '''
        try:
            days_to = args[0].strip(" ").strip(",")
            days_to = int(days_to)
        except IndexError:
            days_to = 7
        # Отримаємо список найближчих іменинників з AddressBook та редагуємо для табличного виводу
        congrats_list = self.book.find_next_week_bithdays(days_to)
        if congrats_list:       
            congrats_list_str = f"Список іменинників на наступні {days_to} днів:".center(56) + f"\n{'-' * 56}\n\
|{'Names':^15}|{'Congratulation date':^25}|{"Days left":^12}|\n{'-' * 56}\n"   
            for item in congrats_list:
                congrats_list_str += f"|{item["name"]:<15}|{item["congratulation_date"]:^25}|{item["days_to_user_congrats"]:^12}|\n"
            congrats_list_str += f"{'-' * 56}"
            return congrats_list_str
        return f"В найближчі {days_to} днів немає іменинників!"

    @error_handler
    def show_all_contacts(self):
        print(self.book)
