from colorama import Fore

from output import output_info, output_warning

from .context import book_cxt_mngr
from .service import PhoneBookService


def bootstrap():
    print(f"{Fore.BLUE}**** Welcome to the assistant bot! ****{Fore.RESET}")
    with book_cxt_mngr() as book:
        book_service = PhoneBookService(book)
        while True:
            command, *args = input("Enter a command: ").strip().lower().split()
            match command:
                case "exit" | "close":
                    print(
                        f"{Fore.BLUE}************** Goodbye! **************{Fore.RESET}"
                    )
                    return
                case "hello":
                    output_info(
                        "Hello! I'm a phone book assistant. How can I help you?"
                    )
                case "add":
                    book_service.add_contact(args)
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
                    book_service.show_next_week_birthdays()
                case "add-email":
                    book_service.add_email(args)

                case "help":
                    print(
                        "Available commands:\n"
                        f"{Fore.CYAN}add {Fore.GREEN}[Name] [Phone Number]{Fore.RESET}- create new record\n"
                        f"{Fore.CYAN}change {Fore.GREEN}[Name] [New Phone Number]{Fore.RESET}- change phone number by [Name]\n"
                        f"{Fore.CYAN}phone {Fore.GREEN}[Phone Number]{Fore.RESET}- display owner name\n"
                        f"{Fore.CYAN}all {Fore.RESET}- list all users with their number\n"
                        f"{Fore.CYAN}add-birthday {Fore.GREEN}[Name] [DD.MM.YYYY]{Fore.RESET}- add to provided contact its birthday\n"
                        f"{Fore.CYAN}show-birthday {Fore.GREEN}[Name]{Fore.RESET}- display contacts birthday\n"
                        f"{Fore.CYAN}birthdays {Fore.RESET}- show contacts which have birthdays in next 7 days\n"
                        f"{Fore.CYAN}help {Fore.RESET}- display commands list\n"
                        f"{Fore.CYAN}exit | close {Fore.RESET}- close the program"
                    )
                case _:
                    output_warning(
                        f"Unknown command: [{Fore.RED}{command}{Fore.RESET}]. Please, use [{Fore.CYAN}help{Fore.RESET}] to see available commands."
                    )
