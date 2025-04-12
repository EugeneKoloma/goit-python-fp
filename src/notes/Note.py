from datetime import datetime as dtdt

from colorama import Fore

from common import Tag

from .NotesFields import Context, Date, Title


class Note:
    def __init__(self, title: str = "Without title", context: str = ""):
        self.title: Title = Title(title)
        self.context: Context = Context(context)
        self.tags: list[Tag] = []
        now = dtdt.now()
        self.created_at: Date = Date(now)
        self.updated_at: Date = Date(now)
        self.__id: int = None

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    def change_title(self, new_title: str):
        self.title._value = new_title
        self.updated_at.date = dtdt.now()

    def change_context(self, new_note: str):
        self.context._value = new_note
        self.updated_at.date = dtdt.now()

    def add_tag(self, tag: str):
        if tag.lower() not in [tag.value for tag in self.tags]:
            self.tags.append(Tag(tag.lower()))
        else:
            print(f"[INFO]: The note with title '{self.tags}' already has such tag!")

    def edit_tag(self, old_tag: str, new_tag: str):
        if self.tags:
            exist_tag = next((tag for tag in self.tags if tag == old_tag.lower()), None)
            if exist_tag:
                self.tags.remove(exist_tag)
                self.tags.append(Tag(new_tag.lower()))
            else:
                print(
                    f"[INFO]: The note with title '{self.title}' doesn't have such tag!"
                )

    def delete_tag(self, tag: str):
        if self.tags:
            exist_tag = next((item for item in self.tags if item == tag.lower()), None)
            if exist_tag:
                self.tags.remove(exist_tag)
            else:
                print(
                    f"[INFO]: The note with title '{self.title}' doesn't have such tag!"
                )

    def __str__(self):
        return f"{Fore.LIGHTBLUE_EX}{self.title}{Fore.RESET}: {self.context} {self.tags} {self.created_at} {self.updated_at}"
