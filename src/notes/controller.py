from colorama import Fore

from common.input_prompts import (
    edit_note_prompt,
    get_new_note_details,
)
from output import output_error

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
                else:
                    context = args[0] if len(args) > 0 else None
                    title = args[1] if len(args) > 1 else None
                    tags = args[2].split(",") if len(args) > 2 else []
                    notes_service.add_note_to_notes_book(
                        {"context": context, "title": title, "tags": tags}
                    )

            case "edit":
                if not args:
                    id, field, new_value = edit_note_prompt(notes)
                    if id and field and new_value:
                        notes_service.update_note_by_id(
                            {"ID": id, field.capitalize(): new_value}
                        )
                else:
                    id = args[0]
                    field = args[1]
                    if field == "tags":
                        old_tags = args[2].split(",") if len(args) > 2 else []
                        notes_service.delete_tags_by_note_id([id, old_tags])
                        new_tags = args[3].split(",") if len(args) > 3 else []
                        notes_service.update_note_by_id({"ID": id, "Tags": new_tags})
                    else:
                        new_value = args[2] if len(args) > 2 else None
                        notes_service.update_note_by_id(
                            {"ID": id, field.capitalize(): new_value}
                        )

            case "remove":
                if len(args) == 2 and args[0] == "tag":
                    note_id, tags = args[1], args[2].split(",")
                    notes_service.delete_tags_by_note_id([note_id, tags])
                elif len(args) == 2 and args[0] == "note":
                    note_id = args[1]
                    notes_service.delete_note_by_id([note_id])
                else:
                    print(f"{Fore.RED}Invalid remove command.{Fore.RESET}")

            case "add-tags":
                if not args:
                    output_error(
                        "Please provide note ID and tags to add. Example: add-tags <note_id> <tag1,tag2>"
                    )
                    return
                if len(args) == 2:
                    tags = args[1].split(",")
                    note_id = args[0]
                    notes_service.add_tags_to_note_by_id(note_id, tags)
                else:
                    output_error(
                        f"Wrong number of atguments. Expected 3, got {len(args)}."
                    )

            case "find":
                if not args:
                    print("Please provide field (by) and query (what) to search.")
                    return
                field = args[0]
                if field not in [
                    "id",
                    "title",
                    "tags",
                    "tag",
                    "context",
                ]:
                    field = "elastic_search"
                query = args[1:]
                match field:
                    case "id":
                        notes_service.find_note_by_id(query)
                    case "title":
                        notes_service.find_notes_by_title(query)
                    case "tags" | "tag":
                        notes_service.find_notes_by_tags(query)
                    case "context":
                        notes_service.find_notes_by_context(query)
                    case "elastic_search":
                        notes_service.elastic_search(query)
                    case _:
                        print(f"{Fore.RED}Unknown field '{field}'.{Fore.RESET}")

            case "export":
                notes_service.export_notes_to_folder(args)
            case "all":
                notes_service.show_all_notes()
            case _:
                output_error(f"Unknown notes command: {action}")

    return commands
