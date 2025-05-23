from common import Tag
from decorators import error_handler
from exceptions import NoteNotFoundError
from output import (
    notes_output,
    output_error,
    output_info,
)

from .Note import Note
from .Notes import Notes
from .NotesFields import Context, Title
from utils.export_import import export_notes_to_folder


class NotesBookService:
    def __init__(self, notes_book: Notes):
        self.__notes_book: Notes = notes_book

    @property
    def notes_book(self):
        return self.__notes_book

    @notes_book.setter
    def notes_book(self, notes_book: Notes):
        self.notes_book = notes_book

    ################################# ADD NOTES SERVICE #################################

    @error_handler
    def add_note_to_notes_book(self, args: dict) -> None:
        # Create a new Note-objext only if context exists
        if args:            
            title = args.get("title", None)  # -> str
            context = args.get("context", None)  # -> str
            tags = args.get("tags", [])  # -> list | str
            if isinstance(tags, str):
                tags = tags.lower().strip(", #").split()

            if context:                
                new_note = Note(context = context)      
                if title:
                    new_note.title = Title(title)
                if tags:
                    new_note.tags = [Tag(tag) for tag in tags]
                
                self.notes_book.add_note(new_note)
                output_info(
                    f"Note with <<id{new_note.id}>> and title <<{new_note.title.value}>> has been added."
                )
            else:
                output_error(
                    "You haven't entered any context for the note (is necessary). Nothing was added!."
                )

    ################################# FIND/SHOW NOTES SERVICES #################################

    @error_handler
    def find_note_by_id(self, args: list[str]) -> dict | None:
        if args:
            # if entered with "id"- preffix
            query = args[0].replace("id", "").strip(", ")
            if self.notes_book.find_notes_by_id(query):
                notes_output(self.notes_book.find_notes_by_id(query))
                return self.notes_book.find_notes_by_id(query)
            raise NoteNotFoundError

    @error_handler
    def find_notes_by_title(self, args: list[str]) -> dict | None:
        query = " ".join(args)
        if query:
            if self.notes_book.find_notes_by_title(query):
                notes_output(self.notes_book.find_notes_by_title(query))
                return self.notes_book.find_notes_by_title(query)
            raise NoteNotFoundError

    @error_handler
    def find_notes_by_tags(self, args: list[str]) -> dict | None:
        if args:
            result = {}
            for query in args:
                if self.notes_book.find_notes_by_tag(query):
                    result.update(self.notes_book.find_notes_by_tag(query))
                notes_output(result)
                return result
            raise NoteNotFoundError

    @error_handler
    def find_notes_by_context(self, args: list[str]) -> dict | None:
        query = " ".join(args)
        if query:
            notes = self.notes_book.find_notes_by_context(query)
            if notes:
                notes_output(notes)
                return notes
            raise NoteNotFoundError

    @error_handler
    def elastic_search(self, args: list[str]) -> dict | None:
        if args:
            result = {}
            for query in args:
                if self.notes_book.find_notes_by_query(query):
                    result.update(self.notes_book.find_notes_by_query(query))
                notes_output(result)
                return result
            raise NoteNotFoundError

    @error_handler
    def show_all_notes(self) -> None:
        if self.notes_book:
            notes_output(self.notes_book.data)
        else:
            output_info("Thera no any notes in NotesBook yet!")

    ################################# UPDATE NOTES SERVICE #################################

    @error_handler
    def update_note_by_id(self, args: dict):
        if args:
            note_id = args.get("ID", None)  # -> str
            new_title = args.get("Title", None)  # -> str
            new_context = args.get("Context", None)  # -> str
            pair_of_tags = args.get("Tags", [])  # -> list
            note = self.notes_book.get(note_id, None)
            if note:
                # If we change only 1 field by inline command will output the warning about empty new value
                if not (new_title or new_context or pair_of_tags) and len(args) <= 2:
                    output_info("Nothing changed, because nothing was entered!")
                else:
                    if new_title:
                        note.change_title(new_title)
                    if new_context:
                        note.change_context(new_context)
                    if pair_of_tags:
                        old_tag, new_tag, *_ = pair_of_tags
                        if new_tag:
                            note.edit_tag(old_tag, new_tag)
                        else:
                            output_info(
                                f"Tag {old_tag} wasn't changed, because new value is absent!"
                                + "If you want to delete tag, use another command!"
                            )
            else:
                raise NoteNotFoundError

    @error_handler
    def add_tags_to_note_by_id(self, note_id: str, tags: list[str]):
        note = self.notes_book.get(note_id, None)
        if note:
            for tag in tags:
                note.add_tag(tag)
            output_info(f"Tags {tags} have been added to note with ID {note_id}.")
        else:
            raise NoteNotFoundError

    ################################# OTHER NOTES SERVICES #################################

    @error_handler
    def delete_note_by_id(self, args: list[str]):
        if args:
            note_id, *_ = args
            self.notes_book.delete_note_by_id(note_id)

    @error_handler
    def delete_tags_by_note_id(self, args: list[str]):
        if args:
            note_id, tags = args
            note_id = note_id.replace("id", "").strip(", ")
            note = self.notes_book.get(note_id, None)
            if note:
                for tag in tags:
                    note.delete_tag(tag)

    @error_handler
    def sort_note_by_date(self, args: list[str]) -> dict | None:
        if args:
            choice, *_ = args
            updated_result = {}
            for id, note in self.notes_book.items():
                updated_result.update({note.updated_at.date: id})
            updated_result_asc = dict(sorted(updated_result.items()))
            updated_result_asc = dict(
                [
                    (value, self.notes_book.data[value])
                    for value in updated_result_asc.values()
                ]
            )
            updated_result_desc = dict(sorted(updated_result.items(), reverse=True))
            updated_result_desc = dict(
                [
                    (value, self.notes_book.data[value])
                    for value in updated_result_desc.values()
                ]
            )
            if choice == "created asc":
                notes_output(dict(self.notes_book.items()))
                return dict(self.notes_book.items())
            elif choice == "created desc":
                notes_output(dict(sorted((self.notes_book.items()), reverse=True)))
                return dict(sorted((self.notes_book.items()), reverse=True))
            elif choice == "updated asc":
                notes_output(updated_result_asc)
                return updated_result_asc
            elif choice == "updated desc":
                notes_output(updated_result_desc)
                return updated_result_desc

    def export_notes_to_folder(self, args: list[str]):
        if args:
            export_notes_to_folder(self.notes_book, args)
        else:
            export_notes_to_folder(self.notes_book)


if __name__ == "__main__":
    pass
