from colorama import Fore
from datetime import datetime as dtdt

from NotesFields import*
# from common import Tag


class Note():

    def __init__(self, note: str):
        self.title: Title = Title("Without title")
        self.note: NoteString = NoteString(note)
        self.tags: list[Tag] = []
        self.creation_time: GetTime = GetTime(dtdt.now())
        self.changin_time: GetTime | None = None
    
    def change_title(self, new_title: str):
        '''
        Change the note's title
        '''
        self.title._value = new_title
        self.changin_time = GetTime(dtdt.now())

    def change_note(self, new_note: str):
        '''
        Change the note's text
        '''
        self.note._value = new_note
        self.changin_time = GetTime(dtdt.now())
    
    def add_tag(self, tag: str):
        '''
        Add a new tag to the Tag-object
        '''
        if tag not in self.tags:
            self.tags.append(tag)
        else:
            print(f"[INFO]: The note with title '{self.tags}' already has such tag!")

    def edit_tag(self, old_tag: str, new_tag: str):
        '''
        Edit existing tag with anouther value
        '''
        if self.tags:
            if old_tag in self.tags:
                self.tags.insert(self.tags.index(old_tag), new_tag)
                self.tags.remove(old_tag)

    def delete_tag(self, tag: str):
        '''
        Delete tag from the Tag-object
        '''
        if self.tags:
            if tag in self.tags:
                self.tags.remove(tag)
    
    def __str__(self):
        return f"{Fore.LIGHTBLUE_EX}{self.title}{Fore.RESET}: {self.note}"