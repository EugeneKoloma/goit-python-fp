from colorama import Fore

from common.input_prompts import edit_contact_prompt, get_contact_details

from .ContactsBook import ContactsBook
from .service import PhoneBookService


def conntroller(book: ContactsBook):
    book_service = PhoneBookService(book)

    def commands(*args):
        action, *args = args
        match action:
            case "add":
                print(f"{Fore.LIGHTBLUE_EX}Adding contact...{Fore.RESET}")
                data = get_contact_details()
                book_service.add_contact_from_dict(data)
            case "edit":
                print(f"{Fore.LIGHTBLUE_EX}Editing contact...{Fore.RESET}")
                name, field, new_value = edit_contact_prompt(book)
                if name and field and new_value:
                    book_service.edit_contact_field(name, field, new_value)
            case "change":
                book_service.change_contacts_phone(args)
            case "phone":
                book_service.show_contacts_phones(args)
            case "all":
                book_service.show_all_contacts()
            case "add-birthday":
                book_service.set_birthday(args)
            case "show-birthday":
                book_service.get_birthday(args)
            case "birthdays":
                print(
                    f"{Fore.LIGHTBLUE_EX}{book_service.show_next_n_days_birthdays(args)}{Fore.RESET}"
                )

    return commands
