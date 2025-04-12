import argparse
import re

from colorama import Fore

from common.input_prompts import (
    edit_contact_prompt,
    get_new_contact_details,
    get_supported_fields,
    is_valid_field,
    prompt_for_field,
    prompt_remove_details,
)
from context import save_data
from output import output_error, output_info, output_warning

from .ContactsBook import ContactsBook
from .service import PhoneBookService
from .undo import load_undo_state


def handle_undo(book: ContactsBook):
    restored_book = load_undo_state()
    if not restored_book:
        output_error("No undo available.")
        return
    save_data(restored_book)
    output_info("Last operation undone.")


# Allow complex values input in quotes like address
def parse_args(raw: str) -> list:
    # Flatten re.findall matches into a single string list
    matches = re.findall(r'"([^"]+)"|(\S+)', raw)
    return [group1 if group1 else group2 for group1, group2 in matches]


def conntroller(book: ContactsBook):  # consider renaming to `controller`
    book_service = PhoneBookService(book)

    def commands(*args):
        if not args:
            return

        action, *args = args
        match action:
            case "add":
                # Convert raw args into a single string and parse respecting quotes
                raw_input = " ".join(args)
                args = parse_args(raw_input)

                if not args:
                    # Full interactive mode
                    data = get_new_contact_details(book)
                    book_service.add_contact_from_dict(data)
                    output_info(f"Created new contact '{data['name'].capitalize()}'")

                elif len(args) == 1:
                    # One field provided: `contacts add phone`
                    field = args[0]
                    if not is_valid_field(field):
                        supported = ", ".join(get_supported_fields())
                        output_error(f"Unknown field. Choose from: {supported}")
                        return

                    if field != "name":
                        name = prompt_for_field("name").strip()

                    if not name:
                        output_error("Contact name is required.")
                        return

                    value = prompt_for_field(field)
                    if not book_service.validate_field(field, value):
                        output_error(f"Invalid value for {field}.")
                        return

                    if book_service.contact_exists(name):
                        book_service.edit_contact_field(name, field, value)
                        output_info(f"Updated {field} for {name}")
                    else:
                        book_service.add_contact_from_dict({"name": name, field: value})
                        output_info(
                            f"Created new contact '{name.capitalize()}' with {field}."
                        )

                elif len(args) == 2:
                    field, value = args

                    if not is_valid_field(field):
                        supported = ", ".join(get_supported_fields())
                        output_error(f"Unknown field. Choose from: {supported}")
                        return

                    if field == "name":
                        name = value
                        contact_data = {"name": name}

                        # Prompt for phone
                        phone = prompt_for_field("phone")
                        if not book_service.validate_field("phone", phone):
                            output_error("Invalid phone number.")
                            return
                        contact_data["phone"] = phone

                        book_service.add_contact_from_dict(contact_data)
                        output_info(f"Created new contact '{name}' with phone.")

                    else:
                        name = prompt_for_field("name").strip()
                        if not name:
                            output_error("Contact name is required.")
                            return

                        if not book_service.validate_field(field, value):
                            output_error(f"Invalid value for {field}.")
                            return

                        contact_data = {"name": name, field: value}

                        # Prompt for phone if not provided
                        if field != "phone":
                            phone = prompt_for_field("phone")
                            if not book_service.validate_field("phone", phone):
                                output_error("Invalid phone number.")
                                return
                            contact_data["phone"] = phone

                        book_service.add_contact_from_dict(contact_data)
                        output_info(f"Created new contact '{name}' with {field}.")

                elif len(args) == 3:
                    # Quick-add mode: `contacts add John phone 1234567`
                    field, value, name = args

                    if not is_valid_field(field):
                        output_error(f"Unknown field '{field}'")
                        return

                    if not book_service.validate_field(field, value):
                        output_error(f"Invalid value for {field}.")
                        return

                    if book_service.contact_exists(name):
                        book_service.edit_contact_field(name, field, value)
                        output_info(f"Updated {field} for {name.capitalize()}")
                    else:
                        contact_data = {"name": name, field: value}

                        # Ensure phone is included
                        if field != "phone":
                            phone = prompt_for_field("phone")
                            if not book_service.validate_field("phone", phone):
                                output_error("Invalid phone format.")
                                return
                            contact_data["phone"] = phone

                        book_service.add_contact_from_dict(contact_data)
                        output_info(
                            f"Created new contact '{name.capitalize()}' with {field}"
                        )

                else:
                    output_error(
                        "Usage:\n"
                        "  contacts add\n"
                        "  contacts add phone\n"
                        "  contacts add [field] [value] [name]"
                    )

            case "edit":
                print(f"{Fore.LIGHTBLUE_EX}Editing contact...{Fore.RESET}")
                field, new_value, name = edit_contact_prompt(book)
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
                    field, value, name = args
                    success = book_service.remove_contact_field(name, field, value)
                    if success:
                        output_info(
                            f"{field.capitalize()} '{value}' removed from {name.capitalize()}."
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
