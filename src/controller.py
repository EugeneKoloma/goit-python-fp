from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

from contacts import cntcts_controller
from context import data_cxt_mngr
from output import output_warning

COMMAND_TREE = {
    "contacts": [
        "add",
        "edit",
        "phone",
        "change",
        "all",
        "birthdays",
        "add-birthday",
        "show-birthday",
    ],
    "notes": ["add", "search", "tag"],
}


class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip().lower()
        parts = text.split()

        if len(parts) == 0:
            for cmd in COMMAND_TREE:
                yield Completion(cmd + " ", start_position=0)
        elif len(parts) == 1:
            for cmd in COMMAND_TREE:
                if cmd.startswith(parts[0]):
                    yield Completion(cmd + " ", start_position=-len(parts[0]))
        elif len(parts) == 2 and parts[0] in COMMAND_TREE:
            for sub in COMMAND_TREE[parts[0]]:
                if sub.startswith(parts[1]):
                    yield Completion(sub, start_position=-len(parts[1]))


def bootstrap():
    init()
    print(f"{Fore.BLUE}**** Welcome to the assistant bot! ****{Fore.RESET}")
    with data_cxt_mngr() as (book, notes):
        contacts_controller = cntcts_controller(book)

        completer = CommandCompleter()

        while True:
            try:
                parts = (
                    prompt("Enter a command: ", completer=completer)
                    .strip()
                    .lower()
                    .split()
                )
                if not parts:
                    print("Empty command")
                    continue

                command, *args = parts

                match command:
                    case "exit" | "close":
                        print(
                            f"{Fore.BLUE}************** Goodbye! **************{Fore.RESET}"
                        )
                        return
                    case "contacts":
                        if args:
                            contacts_controller(*args)
                        else:
                            contacts_controller("all")
                    case "notes":
                        print(
                            f"{Fore.BLUE}************** Notes **************{Fore.RESET}"
                        )
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
            except (EOFError, KeyboardInterrupt):
                print(
                    f"\n{Fore.BLUE}************** Goodbye! **************{Fore.RESET}"
                )
                break


if __name__ == "__main__":
    pass
