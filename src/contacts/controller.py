import argparse
import re
from datetime import datetime as dt

from colorama import Fore

from common.input_prompts import (
    get_new_contact_details,
    get_supported_fields,
    is_valid_field,
    prompt_for_field,
    prompt_remove_details,
)
from context import save_data
from output import (
    output_error,
    output_info,
    output_warning,
    show_contact_card,
)

from .ContactsBook import ContactsBook
from .service import PhoneBookService
from .undo import load_undo_state

global UNDONE
UNDONE = False


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


def select_field_value(record, field: str) -> str | None:
    """
    Returns a single selected value from a multi-valued field like phones, emails, tags.
    If only one value exists, it returns it directly.
    """
    values = record.get_field_values_list(field)

    # Sanity check and normalization
    if isinstance(values, str):
        values = [values]
    elif not isinstance(values, list):
        values = [str(values)]
    else:
        values = [str(v) for v in values]

    if not values:
        output_error(f"No values found in field: {field}")
        return None

    if len(values) == 1:
        return values[0]

    # Multiple values — prompt selection
    print(f"Multiple values found in field '{field}':")
    for idx, val in enumerate(values, start=1):
        print(f"{idx}. {val}")

    try:
        index = int(input("Select value number to edit: "))
        if 1 <= index <= len(values):
            selected = values[index - 1]
            print(f"Selected: {selected}")
            return selected
        else:
            output_error("Invalid selection.")
            return None
    except ValueError:
        output_error("Invalid input. Please enter a number.")
        return None


def conntroller(book: ContactsBook):  # consider renaming to `controller`
    book_service = PhoneBookService(book)

    def commands(*args):
        if not args:
            return

        # Convert raw args into a single string and parse respecting quotes
        raw_input = " ".join(args)
        args = parse_args(raw_input)

        action, *args = args
        match action:
            case "add":
                if not args:
                    # Full interactive mode
                    data = get_new_contact_details(book)
                    book_service.add_contact_from_dict(data)
                    output_info(f"Created new contact '{data['name'].capitalize()}'")

                elif len(args) == 1:
                    # One field provided: `contacts add phone` or `contacts add name`
                    field = args[0]
                    if not is_valid_field(field):
                        supported = ", ".join(get_supported_fields())
                        output_error(f"Unknown field. Choose from: {supported}")
                        return

                    value = prompt_for_field(field).strip()
                    if not book_service.validate_field(field, value):
                        output_error(f"Invalid value for {field}.")
                        return

                    if field == "name":
                        # Only name was provided, so we need to prompt for phone at least
                        name = value
                        phone = prompt_for_field("phone").strip()
                        if not book_service.validate_field("phone", phone):
                            output_error("Invalid phone number.")
                            return
                        if book_service.book.is_phone_owned(phone):
                            output_error(
                                f"Phone number '{phone}' is already associated with another contact."
                            )
                            return
                        if book_service.contact_exists(name):
                            output_error(
                                f"Contact with name '{name}' already exists. Use 'edit' to update the contact."
                            )
                            return
                        book_service.add_contact_from_dict(
                            {"name": name, "phone": phone}
                        )
                        output_info(
                            f"Created new contact '{name.capitalize()}' with phone."
                        )
                    else:
                        # Some other field was provided, so prompt for name
                        if field != "name":
                            name = prompt_for_field("name").strip()

                            if book_service.contact_exists(name):
                                book_service.edit_contact_field(name, field, value)
                                output_info(f"Updated {field} for {name}")
                            else:
                                # Also prompt for phone if not the one being added
                                contact_data = {"name": name, field: value}
                                if field != "phone":
                                    phone = prompt_for_field("phone").strip()
                                    if not book_service.validate_field("phone", phone):
                                        output_error("Invalid phone number.")
                                        return
                                    if book_service.book.is_phone_owned(phone):
                                        output_error(
                                            f"Phone number '{phone}' is already associated with another contact."
                                        )
                                        return
                                    contact_data["phone"] = phone
                                book_service.add_contact_from_dict(contact_data)
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

                        existing_record = book_service.book.find(name)

                        if existing_record and existing_record.phones:
                            contact_data["phone"] = str(existing_record.phones[0])
                        else:
                            # Prompt for phone if no record or no phones
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
                        existing_record = book_service.book.find(name)

                        if existing_record and existing_record.phones:
                            contact_data["phone"] = str(existing_record.phones[0])
                        else:
                            phone = prompt_for_field("phone").strip()
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
                        if field != "phone":
                            phone = prompt_for_field("phone").strip()
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

                if not args:
                    # Full interactive
                    name = prompt_for_field("name")
                    record = book.find(name)
                    if not record:
                        output_error(f"No contact found with name: {name}")
                        return

                    results = book_service.find_contacts(name)
                    from output.rich_table import display_contacts_table

                    display_contacts_table(results)

                    # output_info(f"Editing contact: {record}")

                    field = prompt_for_field("field")
                    if not is_valid_field(field):
                        output_error(f"Unknown field: {field}")
                        return

                    old_value = select_field_value(record, field)
                    if old_value is None:
                        return

                    new_value = prompt_for_field(field)

                elif len(args) == 1:
                    # Semi-interactive
                    field = args[0]
                    if not is_valid_field(field):
                        output_error(f"Unknown field: {field}")
                        return

                    name = prompt_for_field("name")
                    record = book.find(name)
                    if not record:
                        output_error(f"No contact found with name: {name}")
                        return

                    # print(f"Getting old value for {field} in contact {name} 1 arg: {args}")
                    old_value = select_field_value(record, field)
                    # print(f"Old value = {old_value}")
                    if old_value is None:
                        return

                    new_value = prompt_for_field(field)

                elif len(args) == 2:
                    # Direct
                    field, name = args
                    if not is_valid_field(field):
                        output_error(f"Unknown field: {field}")
                        return

                    record = book.find(name)
                    if not record:
                        output_error(f"No contact found with name: {name}")
                        return

                    # print(f"Getting old value for {field} in contact {name} 2 args: {args}")
                    old_value = select_field_value(record, field)
                    # print(f"Old value = {old_value}")
                    if old_value is None:
                        return

                    new_value = prompt_for_field(field)

                else:
                    output_warning(
                        "Invalid arguments. Usage:\n edit\n edit [field]\n edit [field] [name]"
                    )
                    return

                print(f"Trying to update {field} for {name}: {old_value} → {new_value}")
                if not book_service.validate_field(field, new_value):
                    output_error(f"Invalid value for {field}: {new_value}")
                    return

                success = book_service.edit_contact_field(
                    name, field, new_value, old_value=old_value
                )
                if success:
                    output_info(f"{field.capitalize()} updated for {name}")
                else:
                    output_error(f"Failed to update {field} for {name}")

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
                        output_info(
                            f"{field.capitalize()} removed successfully from {name}"
                        )
                    else:
                        output_error(f"Failed to remove {field} from {name}")
                    return

                if args[0] == "contact" and len(args) >= 2:
                    name = " ".join(args[1:])
                    names = book_service.find_contacts(query=name, mode="fuzzy")

                    if not names:
                        output_error(f"No contacts found matching: {name}")
                        return

                    if len(names) == 1:
                        # use the actual matched name
                        actual_name = str(names[0].name)
                        success = book_service.remove_contact(actual_name)
                        name = actual_name  # update for success message
                    else:
                        output_info(f"Found multiple contacts matching '{name}':")
                        for idx, match in enumerate(names, start=1):
                            print(f"{idx}. {match}")

                        try:
                            choice = int(
                                input("Enter the number of the contact to remove: ")
                            )
                            if 1 <= choice <= len(names):
                                selected_name = str(names[choice - 1].name)
                                success = book_service.remove_contact(selected_name)
                                name = selected_name
                            else:
                                output_error("Invalid selection.")
                                return
                        except ValueError:
                            output_error("Invalid input. Please enter a number.")
                            return

                    if success:
                        output_info(f"Contact '{name}' has been removed.")
                    else:
                        output_error(f"Contact '{name}' not found.")

                elif len(args) == 2:
                    field, name = args

                    if field == "contact":
                        names = book_service.find_contacts(query=name, mode="fuzzy")
                        if not names:
                            output_error(f"No contacts found matching: {name}")
                            return

                        if len(names) == 1:
                            actual_name = str(names[0].name)
                            success = book_service.remove_contact(actual_name)
                            name = actual_name
                        else:
                            output_info(f"Found multiple contacts matching '{name}':")
                            for idx, match in enumerate(names, start=1):
                                print(f"{idx}. {match}")
                            try:
                                choice = int(
                                    input("Enter the number of the contact to remove: ")
                                )
                                if 1 <= choice <= len(names):
                                    selected_name = str(names[choice - 1].name)
                                    success = book_service.remove_contact(selected_name)
                                    name = selected_name
                                else:
                                    output_error("Invalid selection.")
                                    return
                            except ValueError:
                                output_error("Invalid input. Please enter a number.")
                                return

                        if success:
                            output_info(f"Contact '{name}' has been removed.")
                        else:
                            output_error(f"Contact '{name}' not found.")

                    else:
                        # Field + name provided, but missing value → prompt
                        value = prompt_for_field(field)
                        success = book_service.remove_contact_field(name, field, value)
                        if success:
                            output_info(
                                f"{field.capitalize()} '{value}' removed from {name.capitalize()}."
                            )
                        else:
                            output_warning(
                                "Nothing was removed. Check the field, value, and name."
                            )

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

            case "sort":
                field = args[0].lower() if args else None
                order = args[1].lower() if len(args) > 1 else "asc"
                reverse = order == "desc"
                valid_fields = ["name", "phone", "email", "address", "birthday", "tags"]

                if not field or field not in valid_fields:
                    return output_error(
                        f"❌ Please provide a valid field to sort by: {', '.join(valid_fields)}"
                    )

                def get_sort_key(record):
                    value = getattr(record, field, None)

                    if field == "birthday":
                        try:
                            # Очікуємо, що value — об'єкт Birthday із .value типу datetime.date або str
                            birthday_val = (
                                value.value if hasattr(value, "value") else value
                            )
                            if isinstance(birthday_val, dt):
                                return birthday_val
                            return dt.strptime(str(birthday_val), "%d.%m.%Y")
                        except Exception:
                            return dt.max  # якщо не вдалося парсити — останнім

                    if isinstance(value, list):
                        return str(value[0]) if value else ""

                    return str(value) if value else ""

                sorted_records = sorted(
                    book.data.values(), key=get_sort_key, reverse=reverse
                )

                if not sorted_records:
                    return output_info("📭 No contacts to show.")
                return book_service.show_sorted_contacts(sorted_records)

            case "phone":
                book_service.show_contacts_phones(args)

            case "all":
                book_service.show_all_contacts(args)

            case "show-birthday":
                book_service.get_birthday(args)

            case "birthdays":
                book_service.show_next_n_days_birthdays(args)

            case "show":
                if not args or len(args) > 1:
                    output_error("Usage: contacts show [NAME]")
                    return

                name = args[0]
                record = book.find(name)
                if not record:
                    output_error(f"No contact found with name: {name}")
                else:
                    show_contact_card(record)

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
                global UNDONE

                if restored and not UNDONE:
                    # Overwrite the passed-in `book` object
                    UNDONE = True
                    book.data = restored.data
                    output_info("Last operation has been undone!")
                else:
                    output_warning("Nothing to undo yet.")

            case "photo":
                if not args:
                    # Prompt for path if missing
                    photo_path = prompt_for_field("Photo path")
                else:
                    # Join args in case of path with spaces (quoted handled by parse_args)
                    photo_path = " ".join(args)

                if not book_service.validate_field("photo", photo_path):
                    output_error("Invalid path. Please provide an existing .txt file.")
                    return

                name = prompt_for_field("name")
                record = book.find(name)
                if not record:
                    output_error(f"Contact '{name}' not found.")
                    return

                # Save the photo path in the record
                record.photo = photo_path
                output_info(f"Photo added to contact '{name}'.")

            case "export":
                book_service.export_contacts_to_csv(args)

            case "import":
                output_warning("All duplicates will be recovered!")
                if input("Confirm import [y]: ") == "y":
                    book_service.import_contacts_to_csv(args)
                else:
                    output_info("Import canceled!")

            case _:
                output_error(f"Unknown contact command: {action}")

    return commands
