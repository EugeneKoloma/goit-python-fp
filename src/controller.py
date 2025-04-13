from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

from contacts import cntcts_controller
from context import data_cxt_mngr
from notes import notes_controller
from output import output_warning
from output.help_ import show_help_panels

COMMAND_TREE = {
    "contacts": [
        "add",
        "add name",
        "add phone",
        "add email",
        "add address",
        "add birthday",
        "add tags",
        "edit",
        "edit name",
        "edit phone",
        "edit email",
        "edit address",
        "edit birthday",
        "edit tags",
        "phone",
        "change",
        "all",
        "birthdays",
        "show-birthday",
        "remove",
        "remove contact",
        "remove phone",
        "remove email",
        "remove address",
        "remove birthday",
        "remove tags",
        "undo",
        "find",
        "show",
        "sort name",
        "sort phone",
        "sort email",
        "sort address",
        "sort birthday",
        "sort tags",
        "export",
        "import",
    ],
    "notes": ["create", "edit", "add", "remove", "find", "all", "export"],
    "help": [],
    "exit": [],
    "close": [],
}

global UNDONE
UNDONE = False


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
        nts_controller = notes_controller(notes)

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
                        if args:
                            nts_controller(*args)
                        else:
                            nts_controller("all")
                    case "help":
                        show_help_panels()
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
