from colorama import Fore

from common.input_prompts import (
    edit_contact_prompt,
    get_new_contact_details,
    get_supported_fields,
    is_valid_field,
    prompt_for_field,
    prompt_missing_args,
    prompt_remove_details,
)
from output import output_error, output_info, output_warning

from .ContactsBook import ContactsBook
from .service import PhoneBookService
from .undo import load_undo_state


def handle_undo(book: ContactsBook):
    restored_book = load_undo_state()
    if not restored_book:
        output_error("No undo available.")
        return
    book = restored_book
    book.save_to_disk()  # Overwrite .bin or .json
    output_info("Last operation undone.")


def conntroller(book: ContactsBook):  # consider renaming to `controller`
    book_service = PhoneBookService(book)

    def commands(*args):
        if not args:
            return

        action, *args = args
        match action:
            case "add":
                if not args:
                    data = get_new_contact_details(book)
                    book_service.add_contact_from_dict(data)

                elif len(args) == 1:
                    field = args[0]
                    if not is_valid_field(field):
                        supported = ", ".join(get_supported_fields())
                        print(
                            f"{Fore.RED}Unknown field. Choose from: {supported}{Fore.RESET}"
                        )
                        return
                    value = prompt_for_field(field)
                    book_service.add_contact_from_dict({field: value})

                elif len(args) == 3:
                    name, field, value = args
                    if not is_valid_field(field):
                        print(f"{Fore.RED}Unknown field '{field}'.{Fore.RESET}")
                        return
                    if not book_service.validate_field(field, value):
                        print(f"{Fore.RED}Invalid value for {field}.{Fore.RESET}")
                        return

                    if book_service.contact_exists(name):
                        book_service.edit_contact_field(name, field, value)
                        print(f"{Fore.GREEN}Updated {field} for {name}{Fore.RESET}")
                    else:
                        # Create new contact with name and one field
                        contact_data = {"name": name, field: value}
                        book_service.add_contact_from_dict(contact_data)
                        print(
                            f"{Fore.GREEN}Created new contact '{name}' with {field}.{Fore.RESET}"
                        )

                else:
                    print(
                        f"{Fore.RED}Usage:\\n"
                        f"  contact add\\n"
                        f"  contact add phone\\n"
                        f"  contact add <name> <field> <value>{Fore.RESET}"
                    )

            case "edit":
                print(f"{Fore.LIGHTBLUE_EX}Editing contact...{Fore.RESET}")
                name, field, new_value = edit_contact_prompt(book)
                if name and field and new_value:
                    if not book_service.validate_field(field, new_value):
                        output_error(f"Invalid value for {field}: {new_value}")
                        return

                    book_service.edit_contact_field(name, field, new_value)
                    output_info(f"{field.capitalize()} updated for {name}")

            case "change":
                book_service.change_contacts_phone(args)

            case "delete":
                print("Delete!")  # Put real delete function here

            case "remove":
                if not args:
                    name, field, value = prompt_remove_details(book)

                    if not field:
                        return

                    if field == "contact":
                        success = book_service.remove_contact(name)
                    else:
                        success = book_service.remove_contact_field(name, field, value)

                    if success:
                        print(
                            f"{Fore.GREEN}{field.capitalize()} removed successfully from {name}.{Fore.RESET}"
                        )
                    else:
                        print(
                            f"{Fore.RED}Failed to remove {field} from {name}.{Fore.RESET}"
                        )
                    return

                if args[0] == "contact" and len(args) == 2:
                    _, name = args
                    success = book_service.remove_contact(name)
                    if success:
                        output_info(f"Contact '{name}' has been removed.")
                    else:
                        output_error(f"Contact '{name}' not found.")
                elif len(args) == 3:
                    name, field, value = args
                    success = book_service.remove_contact_field(name, field, value)
                    if success:
                        output_info(
                            f"{field.capitalize()} '{value}' removed from {name}."
                        )
                    else:
                        output_warning(
                            "Nothing was removed. Check if the value and name are correct."
                        )
                else:
                    output_warning(
                        "Nothing was removed. Check if the value and name are correct."
                    )

            case "phone":
                book_service.show_contacts_phones(args)

            case "all":
                book_service.show_all_contacts(args)

            case "add-birthday":
                provided = {}
                if len(args) > 0:
                    provided["name"] = args[0]
                if len(args) > 1:
                    provided["birthday"] = args[1]

                filled = prompt_missing_args(["name", "birthday"], provided)
                book_service.set_birthday([filled["name"], filled["birthday"]])

            case "show-birthday":
                book_service.get_birthday(args)

            case "birthdays":
                print(
                    f"{Fore.LIGHTBLUE_EX}{book_service.show_next_n_days_birthdays(args)}{Fore.RESET}"
                )

            case "find":
                if not args:
                    print(
                        "Usage: contacts find [--name NAME] [--phone PHONE] [--email EMAIL] [--birthday BIRTHDAY] [--tag TAG] or just search text"
                    )
                    return

                import argparse

                parser = argparse.ArgumentParser(prog="contacts find", add_help=False)
                parser.add_argument("--name")
                parser.add_argument("--phone")
                parser.add_argument("--email")
                parser.add_argument("--birthday")
                parser.add_argument("--tag")

                try:
                    ns, remaining = parser.parse_known_args(args)

                    filters = {}
                    if ns.name:
                        filters["name"] = ns.name
                    if ns.phone:
                        filters["phone"] = ns.phone
                    if ns.email:
                        filters["email"] = ns.email
                    if ns.birthday:
                        filters["birthday"] = ns.birthday
                    if ns.tag:
                        filters["tag"] = ns.tag

                    query = " ".join(remaining).strip()

                    results = book_service.find_contacts(
                        query=query, mode="smart", **filters
                    )

                    if results:
                        from output import display_contacts_table

                        display_contacts_table(results)
                    else:
                        print("No matching contacts found.")

                except Exception as e:
                    print(f"Error while parsing or searching: {e}")

            case "undo":
                restored = load_undo_state()
                if restored:
                    # Overwrite the passed-in `book` object
                    book.data = restored.data
                    output_info("Last operation has been undone!")
                else:
                    output_warning("Nothing to undo yet.")

            case _:
                output_error(f"Unknown contact command: {action}")

    return commands
