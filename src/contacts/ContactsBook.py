from collections import UserDict
from datetime import datetime as dtdt
from datetime import timedelta as td
from typing import Dict

from colorama import Fore

from .ContactFields import Birthday
from .Records import Record

from common import Tag
from exceptions import RecordNotFound, TagNotFound

class ContactsBook(UserDict):
    def __init__(self):
        self.data: Dict[str, Record] = {}

    def add_record(self, record: Record):
        self.data[record.name._value] = record

    def find(self, name: str) -> Record | None:
        if name not in self.data.keys():
            return None
        return self.data[name]

    def is_phone_owned(self, phone: str):
        all_phones = [
            phone.value for record in self.data.values() for phone in record.phones
        ]
        return bool(phone in all_phones)

    def delete(self, name):
        self.data.pop(name)

    def find_next_n_days_bithdays(self, days_to: int = 7) -> list[dict]:
        '''
        Функція повернутає список всіх, у кого день народження вперед на days_to днів включаючи поточний день
        (за замовченням - 7 днів).
        '''
        date_format_pattern = Birthday.date_format_pattern
        today = dtdt.today().date()
        congrats_list = []
        # Проходимося по списку та аналізуємо дати народження кожного користувача
        for name, record in self.data.items():
            if not record.birthday:
                continue
            # Перетворюємо формат дати народження зі строки на дату
            user_birthday = dtdt.strptime(record.birthday.value, date_format_pattern).date()
            user_birthday_this_year = user_birthday.replace(year = today.year)
            # Перевіряємо, чи вже минув день народження в цьому році
            if user_birthday_this_year < today:
                user_birthday_this_year = user_birthday.replace(year = today.year + 1)
            # Визначаємо різницю між днем народження та поточним днем
            days_to_user_birthday_this_year = user_birthday_this_year.toordinal() - today.toordinal()
            # Відбираємо тих, чий день народження відбувається протягом наступного тижня
            if days_to_user_birthday_this_year < days_to:
                user_congrats_day = today + td(days = days_to_user_birthday_this_year)
                user_congrats_day = user_congrats_day.strftime("%d %B %Y, %A")
                if days_to_user_birthday_this_year == 0:
                    days_to_user_birthday_this_year = f"{Fore.LIGHTRED_EX}{'Today!':^12}{Fore.LIGHTBLUE_EX}"
                elif days_to_user_birthday_this_year == 1:
                    days_to_user_birthday_this_year = f"{Fore.LIGHTRED_EX}{'Tomorrow!':^12}{Fore.LIGHTBLUE_EX}"
                congrats_list.append({"name": name, 
                                 "congratulation_date": user_congrats_day,
                                 "days_to_user_congrats": days_to_user_birthday_this_year,})                
        return congrats_list

    # Add tag to contact with exception RecordNotFound raised if no such contact
    def add_tag_to_contact(self, name: str, tag: Tag):
        record = self.get(name)
        if record:
            record.add_tag(tag)
        else: 
            raise RecordNotFound(f"Contact with name '{name}' not found.")

    # Shoe tags from contacts
    def list_tags_for_contact(self, name: str):
        record = self.get(name)
        return record.list_tags() if record else []

    # Delete tag from contact with exception TagNotFound raised if no such tag
    def remove_tag_from_contact(self, name: str, tag: Tag):
        record = self.get(name)
        if not record:
            raise RecordNotFound(f"Contact with name '{name}' not found.")
        if tag not in record.tags:
            raise TagNotFound(tag.value())
        record.remove_tag(tag)

    def __str__(self):
        if not self.data:
            return "Phone book is empty"
        return "\n".join(str(record) for record in self.data.values())
