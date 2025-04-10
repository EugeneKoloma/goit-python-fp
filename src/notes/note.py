from datetime import datetime as dtdt

from colorama import Fore
from NotesFields import Context, Date, Title

from common import Tag


class Note:
    def __init__(self, title: str = "Without title", note: str = ""):
        self.title: Title = Title(title)
        self.context: Context = Context(note)
        self.tags: list[Tag] = []
        now = dtdt.now()
        self.created_at: Date = now
        self.updated_at: Date = now

    def change_title(self, new_title: str):
        self.title._value = new_title
        self.updated_at = dtdt.now()

    def change_context(self, new_note: str):
        self.context._value = new_note
        self.updated_at = dtdt.now()

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)
        else:
            print(f"[INFO]: The note with title '{self.tags}' already has such tag!")

    def edit_tag(self, old_tag: str, new_tag: str):
        if self.tags:
            if old_tag in self.tags:
                self.tags.insert(self.tags.index(old_tag), new_tag)
                self.tags.remove(old_tag)

    def delete_tag(self, tag: str):
        if self.tags:
            if tag in self.tags:
                self.tags.remove(tag)

    def __str__(self):
        return f"{Fore.LIGHTBLUE_EX}{self.title}{Fore.RESET}: {self.context} {self.tags} {self.created_at} {self.updated_at}"
