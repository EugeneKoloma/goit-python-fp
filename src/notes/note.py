"""
Usage example:

    from notes.note import Note

    note = Note([note] (necessary), [Tag-object] (default - '[]'), [note title] (optional, default - "Without title")) -> Dict

    note_1 = Note("Lorems #isput, likes my #shorts")

    print(note_1)  # Outputs colored: # {"Title": "Without title", 
                                        "Note": "Lorems #isput, likes my #shorts", 
                                        "Tags": ["isput", "shorts"]}

    Uses own methods for editing:
        change_title([new title]) - Change the note's title
        change_note([new note's text]) - Change the note's text
        add_tag([new tag]); edit_tag([old tag], [new tag]); delete_tag([tag]) - Editing tags
"""

from collections import UserDict
from colorama import Fore

from common.tag import Tag


class Note(UserDict):

    note_id = 0
    def __init__(self, note: str, tags: Tag = [], title: str = "Without title"):
        Note.note_id += 1
        self.title = title
        self.note = note
        self.tags = tags  
        self.__get_tags_from_note()    
        # Make unique id          
        self.id = "id" + str(Note.note_id)
        # Make a dictioanary
        self.data = {
            "Title": self.title,
            "Note": self.note,
            "Tags": self.tags,
        }      

    @property
    def value(self) -> dict:
        return self.data

    def __get_tags_from_note(self) -> Tag:
        '''
        Gets tags from note, if signed with '#'
        '''
        if self.note:
            for string in self.note.split():
                if string.startswith("#"):
                    self.tags.append(string[1:].strip(",.:;!?'"))
            # After addin tags from note to the tag-object remove '#' from note
            self.note = self.note.replace("#", "")
        return self.tags
    
    def change_title(self, new_title: str):
        '''
        Change the note's title
        '''
        self.data["Title"] = new_title

    def change_note(self, new_note: str):
        '''
        Change the note's text
        '''
        self.data["Note"] = new_note
    
    def add_tag(self, tag: str):
        '''
        Add a new tag to the Tag-object
        '''
        if tag not in self.data["Tags"]:
            self.data["Tags"].append(tag)
        else:
            print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} The note with title '{Fore.LIGHTYELLOW_EX}{self.data["Title"]}{Fore.RESET}' already has such tag!")

    def edit_tag(self, old_tag: str, new_tag: str):
        '''
        Edit existing tag with anouther value
        '''
        if self.data["Tags"]:
            if old_tag in self.data["Tags"]:
                self.data["Tags"].insert(self.data["Tags"].index(old_tag), new_tag)
                self.data["Tags"].remove(old_tag)

    def delete_tag(self, tag: str):
        '''
        Delete tag from the Tag-object
        '''
        if self.data["Tags"]:
            if tag in self.data["Tags"]:
                self.data["Tags"].remove(tag)
    
    def __str__(self):
        return f"{Fore.LIGHTBLUE_EX}{self.value}{Fore.RESET}"