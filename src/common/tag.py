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


class Tag:
    def __init__(self, value: str):
        self._value = value.lower().strip()

    @property
    def tag(self):
        return self.__str__

    def __str__(self):
        return f"#{self._value}"

    def __eq__(self, other):
        if isinstance(other, Tag) and self._value == other._value:
            return True
        if isinstance(other, str) and self._value == other:
            return True
        return False

    def __hash__(self):
        return hash(self._value)

    def value(self):
        return self._value