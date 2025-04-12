from colorama import Fore

from common.input_prompts import (
    edit_note_prompt,
    get_new_note_details,
    # get_supported_note_fields,
    is_valid_note_field,
)
from output import display_notes_table, output_error

from .Notes import Notes
from .service import NotesBookService


def controller(notes: Notes):
    notes_service = NotesBookService(notes)

    def commands(*args):
        if not args:
            return

        action, *args = args
        match action:
            case "create":
                if not args:
                    data = get_new_note_details()
                    notes_service.add_note_to_notes_book(data)

            case "edit":
                if not args:
                    print(f"Notes {notes}")
                    id, field, new_value = edit_note_prompt(notes)
                    if id and field and new_value:
                        pass
                        # notes_service.edit_note_field(note_id, field, new_value)
                else:
                    id, field, value = args
                    if not is_valid_note_field(field):
                        print(f"{Fore.RED}Unknown field '{field}'.{Fore.RESET}")
                        return
                    # notes_service.edit_note_field(note_id, field, value)

            case "remove":
                if len(args) == 2 and args[0] == "tags":
                    # note_id, tags = args[1], args[2]
                    # notes_service.remove_tags_from_note(note_id, tags.split(","))
                    # elif len(args) == 1:
                    # note_id = args[0]
                    # notes_service.remove_note_by_id(note_id)
                    # else:
                    print(f"{Fore.RED}Invalid remove command.{Fore.RESET}")

            case "find":
                if not args:
                    print("Please provide a query to search.")
                    return

                # query = args[0]
                field = args[1] if len(args) > 1 else "all"
                # results = [] # notes_service.find_notes(query)

                # if results:
                #     from output.rich_table import display_notes_table

                #     display_notes_table(results)
                # else:
                #     print(
                #         f"{Fore.YELLOW}No notes found matching: {query}{Fore.RESET}"
                #     )

            # case "undo":
            #     restored = load_undo_state()
            #     if restored:
            #         book.data = restored.data
            #         output_info("Last operation has been undone!")
            #     else:
            #         output_warning("Nothing to undo yet.")

            case "all":
                # notes_service.show_all_notes()
                if notes.data:
                    display_notes_table(notes.data.values())
                else:
                    print(f"{Fore.LIGHTRED_EX}There are no any note yet!{Fore.RESET}")

            case _:
                output_error(f"Unknown notes command: {action}")

    return commands
