from colorama import Fore

from common.input_prompts import (
    edit_contact_prompt,
    get_new_contact_details,
    get_supported_fields,
    is_valid_field,
    prompt_for_field,
)

from .ContactsBook import ContactsBook
from .service import PhoneBookService


def conntroller(book: ContactsBook):  # consider renaming to `controller`
    book_service = PhoneBookService(book)

    def commands(*args):
        if not args:
            return

        action, *args = args
        match action:
            case "add":
                if not args:
                    print(f"{Fore.LIGHTBLUE_EX}Adding contact...{Fore.RESET}")
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
                    book_service.edit_contact_field(name, field, new_value)

            case "change":
                book_service.change_contacts_phone(args)

            case "delete":
                print("Delete!")  # Put real delete function here

            case "remove":
                book_service.remove_contact_field(*args)

            case "phone":
                book_service.show_contacts_phones(args)

            case "all":
                book_service.show_all_contacts()

            case "add-birthday":
                from common.input_prompts import prompt_missing_args

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

            case _:
                print(f"{Fore.RED}Unknown contact command: {action}{Fore.RESET}")

    return commands
