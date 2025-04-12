"""
Usage example:

    from Notes import Notes

    Notes-object uses his own methods to change his instance.
    notes = Note()

    To add a note-objects to the Notes:
    notes.add_note([note-object])

    To find a note-objects in the Notes by id, text or tag:
    notes.find_notes_by_id([note-id])
    notes.find_notes_by_query([some text in note])
    notes.find_notes_by_tag([tag from Tag-object])

    To delete a note-objects from the Notes by id or title:
    notes.delete_note_by_id([note-id])

    Represents the dictionary of pairs 'note-id: note'
"""

from collections import UserDict
from typing import Dict

from colorama import Fore

from exceptions import NoteNotFoundError

from .Note import Note


class Notes(UserDict):
    def __init__(self):
        self.__notes_counter = 0
        self.data: Dict[str, Note] = {}

    def add_note(self, note: Note):
        self.__notes_counter += 1
        note.id = self.__notes_counter
        self.data[str(self.__notes_counter)] = note

    def find_notes_by_id(self, id: str) -> dict:
        return {id: self.data[id]}

    def find_notes_by_context(self, query: str) -> dict:
        query = query.lower()
        result = [
            (id, note)
            for id, note in self.data.items()
            if query in note.context._value.lower()
        ]
        return dict(result)

    def find_notes_by_query(self, query: str) -> dict:
        query = query.lower()
        result = [
            (id, note)
            for id, note in self.data.items()
            if query
            in " ".join(
                [
                    note.title._value,
                    note.context._value,
                    " ".join([tag._value for tag in note.tags]),
                ]
            ).lower()
        ]
        return dict(result)

    def find_notes_by_title(self, query: str) -> dict:
        query = query.lower()
        result = [
            (id, note)
            for id, note in self.data.items()
            if query in note.title._value.lower()
        ]
        return dict(result)

    def find_notes_by_tag(self, tag: str) -> dict:
        tag = tag.lower()
        result = [
            (id, note)
            for id, note in self.data.items()
            if tag in " ".join([tag._value for tag in note.tags]).lower()
        ]
        return dict(result)

    def delete_note_by_id(self, id: str):
        if id in self.data.keys():
            self.data.pop(id)
        else:
            raise NoteNotFoundError

    def __str__(self):
        return (
            f"{Fore.LIGHTBLUE_EX}{self.data}{Fore.RESET}"
            if self.data.items()
            else f"{Fore.LIGHTRED_EX}There are no any note yet!{Fore.RESET}"
        )

    def __setstate__(self, state):
        self.__dict__.update(state)
        if "__notes_counter" not in state:
            self.__notes_counter = 0

    def __getstate__(self):
        state = self.__dict__.copy()
        state["__notes_counter"] = self.__notes_counter
        return state
