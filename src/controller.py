from colorama import Fore, init

from common import data_cxt_mngr
from contacts import cntcts_controller
from output import output_warning


def bootstrap():
    init()
    print(f"{Fore.BLUE}**** Welcome to the assistant bot! ****{Fore.RESET}")
    with data_cxt_mngr() as (book, notes):
        contacts_controller = cntcts_controller(book)
        # notes_controller = notes_controller(notes)
        while True:
            command, *args = input("Enter a command: ").strip().lower().split()
            match command:
                case "exit" | "close":
                    print(
                        f"{Fore.BLUE}************** Goodbye! **************{Fore.RESET}"
                    )
                    return
                case "contacts":
                    contacts_controller(*args)
                case "notes":
                    print(f"{Fore.BLUE}************** Notes **************{Fore.RESET}")
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


if __name__ == "__main__":
    pass
