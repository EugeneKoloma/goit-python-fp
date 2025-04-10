from colorama import Fore

from .ContactsBook import ContactsBook
from .service import PhoneBookService


def conntroller(book: ContactsBook):
    book_service = PhoneBookService(book)

    def commands(*args):
        action, *args = args
        match action:
            case "add":
                print(f"{Fore.LIGHTBLUE_EX}Adding contact...{Fore.RESET}")
                # book_service.add_contact(args)
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
