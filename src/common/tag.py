"""
Clean, reusable, and easy to import anywhere Tag class

Tag class is used to assign colored tags to various domain models like Contacts, Notes or other.
It is designed to be reusable across the project.

Usage example:

    from common.tag import Tag

    tag1 = Tag("work")
    tag2 = Tag("urgent")

    print(tag1)  # Outputs colored: #work
    print(tag2)  # Outputs colored: #urgent

    contact.add_tag(tag1)
    contact.add_tag(tag2)
    print(contact.list_tags())
"""

from colorama import Fore

class Tag:
    def __init__(self, value: str):
        self._value = value.strip()

    def __str__(self):
        return f"{Fore.CYAN}#{self._value}{Fore.RESET}"

    def __eq__(self, other):
        return isinstance(other, Tag) and self._value == other._value

    def __hash__(self):
        return hash(self._value)

    def value(self):
        return self._value