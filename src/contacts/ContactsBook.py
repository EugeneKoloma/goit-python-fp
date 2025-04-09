from collections import UserDict
from datetime import datetime as dtdt
from datetime import timedelta as td
from typing import Dict

from colorama import Fore

from .ContactFields import Birthday
from .Records import Record


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

    def __str__(self):
        if not self.data:
            return "Phone book is empty"
        return "\n".join(str(record) for record in self.data.values())
