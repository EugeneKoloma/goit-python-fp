from collections import UserDict

from common import Field
# from Tags import Tags

class Note:
    def __init__(self, note: str, tags: list[str] = [], title: str = "Without title"):
        self.title = title
        self.note = note
        self.tags = tags
        Note.note_id += 1

    @property
    def value(self):
        return {
            "Title": self.title,
            "Note": self.note,
            "Tags": self.tags,
        }

    def __str__(self):
        pass



class Notes(UserDict):

    def add_record(self, note: Note):
        self.data[note.title] = note

    def find_notes_by_query(self, query) -> list[Note]:
        query = query.lower()
        return [note for note in self.data.values() if query in note["Title"] | note["Note"] | note["Tags"]]
    