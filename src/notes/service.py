from decorators import error_handler
from exceptions import NoteNotFoundError

from output import (
    output_info,
    output_warning,
    output_error,
    notes_output,
)

from common import Tag
from Note import Note
from Notes import Notes
from NotesFields import*


class NotesBookService:
    def __init__(self, notes_book: Notes):
        self.__notes_book: Notes = notes_book

    @property
    def notes_book(self):
        return self.__notes_book

    @notes_book.setter
    def notes_book(self, notes_book: Notes):
        self.notes_book = notes_book

    @error_handler
    def add_note_to_notes_book(self, args: list[str]) -> None:       
        # Create a new Note-objext only if context exists
        if args:
            # Make a note only by context with default title "Without title"
            context = " ".join(args)
            if context:
                new_note = Note()         
            new_note.context = Context(context)
        else:
            title = input("[Optional. Default = 'Without title'] Note's title: ")
            context = input("[Necessary] Your note: ")
            tags = input("[Optional] Tags: ").lower().strip(" ,").split()   

            if context:
                new_note = Note()  
                new_note.context = Context(context)
                if title:
                    new_note.title = Title(title)
                new_note.tags = [Tag(tag) for tag in tags]

        if context:            
            self.notes_book.add_note(new_note)
            output_info(
                    f"Note with <<id{list(self.notes_book.data.keys())[-1]}>> and title <<{new_note.title.value}>> has been added."
                )
        else:
            output_error(
                    f"You haven't entered any context for the note (is necessary). Nothing was added!."
                )

    @error_handler       
    def find_notes(self, args: list[str]): #-> list[Note] | str
        if not args:
            while True:    
                choise = input("Enter a note's param, which must be used for search\n[id | tag | any text - default | cancel]").lower().strip(", ")
                if choise == "id":
                    quary = input("Enter a valid note's id: ")
                    quary = quary.replace("id", "").strip(", ")
                    if self.notes_book.find_notes_by_id(quary):
                        notes_output(self.notes_book.find_notes_by_id(quary))
                        return self.notes_book.find_notes_by_id(quary)
                    raise NoteNotFoundError  
                
                elif choise == "tag":
                    quary = input("Enter a valid tag: ")
                    if self.notes_book.find_notes_by_tag(quary):
                        notes_output(self.notes_book.find_notes_by_tag(quary))
                        return self.notes_book.find_notes_by_tag(quary)
                    raise NoteNotFoundError 
                
                elif choise == "any":
                    quary = input("Enter a query: ")
                    if self.notes_book.find_notes_by_query(quary):
                        notes_output(self.notes_book.find_notes_by_query(quary)   )
                        return self.notes_book.find_notes_by_query(quary)    
                    raise NoteNotFoundError    
               
                elif choise == "cancel": 
                    break
                else:
                    output_warning(
                        "Incorrect choice! Please, repeat!"
                    )
        
        else:
            quary = " ".join(args)
            if quary.lower().startswith("id") or quary.isdigit():
                quary = quary.replace("id", "").strip(", ")
                notes_output(self.notes_book.find_notes_by_id(quary))
                return self.notes_book.find_notes_by_id(quary)
            if self.notes_book.find_notes_by_tag(quary):
                notes_output(self.notes_book.find_notes_by_tag(quary))
                return self.notes_book.find_notes_by_tag(quary)
            if self.notes_book.find_notes_by_query(quary):
                notes_output(self.notes_book.find_notes_by_query(quary))
                return self.notes_book.find_notes_by_query(quary)    
            raise NoteNotFoundError   
                        
    @error_handler  
    def update_note_by_id(self, args: list[str]):

        def change_title(note: Note):
            new_title = input(f"[Optional. Now - '{note.title.value}'] New note's title: ")
            if new_title:
                note.change_title(new_title)
            else:
                output_info(
                    "You haven't entered anything. Title not changed!"
                )

        def change_context(note: Note):
            output_info(
                "You are going to change next note. You can use it's context to copy:"
                + f"\n{'*' * 20}\n{note.context.value}\n{'*' * 20}"
            )
            new_context = input("[Necessary for changes] Your new note's context: ")            
            if new_context:
                note.change_context(new_context)
            else:
                output_info(
                    "You haven't entered anything. Context not changed!"
                )

        def change_tags(note: Note):
            tags_choice = input("Would you like add new or change/delete some of existing tags?\n[add | change | delete | cancel]: ").lower().strip(", ")
            while True:
                if tags_choice == "add":
                    new_tags = input("Enter new tags: ").lower().strip(" ,").split()                    
                    for new_tag in new_tags:
                        note.add_tag(new_tag)

                elif tags_choice == "change":
                    old_tag, new_tag, *_ = input("Enter tags for change [old, new]: ").lower().strip(" ,").split()
                    note.edit_tag(old_tag, new_tag)

                elif tags_choice == "delete":
                    tag = input("Enter tag to delete: ").lower().strip(" ,")
                    note.delete_tag(tag)

                elif tags_choice == "cancel":
                    break
                else:
                    output_warning(
                        "Incorrect choice! Please, repeat!"
                    )

        old_note_id, *_ = args  
        note = self.notes_book.get(old_note_id, None)
        if note:
            choice = input("What are you going to change?\n[title | context | tags | all - default | cancel]: ").lower().strip(", ")
            while True:
                if choice == "title":
                    change_title(note)
                elif choice == "context":
                    change_context(note)
                elif choice == "tags":
                    change_tags(note)
                elif choice == "" or "all":
                    change_title(note)
                    change_context(note)
                    change_tags(note)
                elif choice == "cancel":
                    break
                else:
                    output_warning(
                        "Incorrect choice! Please, repeat!"
                    )
        else:
            raise NoteNotFoundError                                   
        
    @error_handler  
    def delete_note_by_id(self, args: list[str]):
        note_id, *_ = args
        self.notes_book.delete_note_by_id(note_id)

    @error_handler  
    def sort_note_by_date(self) -> dict:
        updated_result = {}
        for id, note in self.notes_book.items():
            updated_result.update({note.updated_at.date: id})
        updated_result_asc = dict(sorted(updated_result.items()))
        updated_result_asc = dict([(value, self.notes_book.data[value]) for value in updated_result_asc.values()])
        updated_result_desc = dict(sorted(updated_result.items(), reverse=True))
        updated_result_desc = dict([(value, self.notes_book.data[value]) for value in updated_result_desc.values()])
        while True:
            choice = input("Enter a needed date (created or updated) with order (asc, desc)\n[created asc | created desc | updated asc | updated desc | cancel]: ").lower().strip()
            if choice == "created asc":
                notes_output(dict(self.notes_book.items())) 
                return dict(self.notes_book.items())
            elif choice == "created desc":
                notes_output(dict(sorted((self.notes_book.items()), reverse=True))  )
                return dict(sorted((self.notes_book.items()), reverse=True))        
            elif choice == "updated asc":
                notes_output(updated_result_asc)
                return updated_result_asc
            elif choice == "updated desc":   
                notes_output(updated_result_desc)            
                return updated_result_desc
            elif choice == "cancel":
                    break
            else:
                output_warning(
                        "Incorrect choice! Please, repeat!"
                    )



if __name__ == "__main__":
    pass