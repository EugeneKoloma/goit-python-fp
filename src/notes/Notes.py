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
from Note import Note

from exceptions import NoteNotFoundError


class Notes(UserDict):
    note_id = 0

    def __init__(self):
        self.data: Dict[str, Note] = {}

    def add_note(self, note: Note):
        Notes.note_id += 1
        self.data[str(Notes.note_id)] = note

    def find_notes_by_id(self, id: str) -> dict:
        return {id: self.data[id]}

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
