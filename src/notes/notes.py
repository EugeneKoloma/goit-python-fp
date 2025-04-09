"""
Usage example:

    from notes.notes import Notes

    Notes-object uses his oun methods to change his instance.
    notes = Note()

    To add a note-objects to the Notes:
    notes.add_note([note-object])

    To find a note-objects in the Notes by id, text or tag:
    notes.find_notes_by_id([note-id])
    notes.find_notes_by_query([some text in note])
    notes.find_notes_by_tag([tag from Tag-object])

    To delete a note-objects from the Notes by id or title:
    notes.delete_note_by_id([note-id])
    notes.delete_note_by_title([note-title])

    Represents the dictionary of pairs 'note-id: note'
"""

from collections import UserDict
from colorama import Fore

from .note import Note


class Notes(UserDict):

    def add_note(self, note: Note):
        '''
        Add a new note to the NotesBook
        '''
        self.data[note.id] = note

    def find_notes_by_id(self, id: str) -> Note:
        '''
        Returns a note, found by its id
        '''
        id = id.lower()
        if id in self.data.keys():
            return self.data[id]

    def find_notes_by_query(self, query: str) -> list[Note]:
        '''
        Returns a list of notes, found by coincidences in their text-note
        '''
        query = query.lower()        
        return [note for note in self.data.values() if query in \
                " ".join([note["Title"], note["Note"], " ".join(note["Tags"])])] \
                    or f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} There is no any coincidences by '{Fore.LIGHTYELLOW_EX}{query}{Fore.RESET}' among our Notes!"
        
    def find_notes_by_tag(self, tag: str) -> list[Note]:
        '''
        Returns a list of notes, found by coincidences in their tags
        '''
        tag = tag.lower()           
        return [note for note in self.data.values() if tag in " ".join(note["tags"]).lower()] \
        or f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} There is no any coincidences by tag '{Fore.LIGHTYELLOW_EX}{tag}{Fore.RESET}' among our Notes!"
    
    def delete_note_by_id(self, id: str):
        '''
        Returns a NotesBook without note, found by its id
        '''
        if id in self.data.keys():
            self.data.pop(id)
            return self.data
        return f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} There is no note with {Fore.LIGHTYELLOW_EX}{id}{Fore.RESET}!"

    def delete_note_by_title(self, title: str):
        '''
        Returns a NotesBook without notes, found by their title
        '''
        # Make a copy of NotesBook for deleting coincidences
        temp_data = self.data.copy()
        for id, note in self.data.items():
            if title.lower() == note["Title"].lower():
                temp_data.pop(id)
        # return edited data to the NotesBook end remove temp data
        self.data = temp_data.copy()
        del temp_data
        return self.data or f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} There is no notes with title '{Fore.LIGHTYELLOW_EX}{title}{Fore.RESET}'!"
    
    def __str__(self):
        return f"{Fore.LIGHTBLUE_EX}{self.data}{Fore.RESET}"