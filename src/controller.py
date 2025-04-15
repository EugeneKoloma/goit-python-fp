import os
import random
import time

from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.text import Text

from contacts import cntcts_controller
from context import data_cxt_mngr
from notes import notes_controller
from output import output_warning
from output.help_ import show_help_ascii_tree, show_help_panels
from tests.test_contacts import run_all_tests

console = Console()

COMMAND_TREE = {
    "contacts": [
        "add",
        "add name",
        "add phone",
        "add email",
        "add address",
        "add birthday",
        "add tags",
        "add photo",
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
    "notes": ["create", "edit", "add-tags", "remove", "find", "all", "export"],
    "help": [],
    "help-tree": [],
    "test-contacts": [],
    "exit": [],
    "close": [],
}

global UNDONE
UNDONE = False

MATRIX_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#$%^&*()"

# Optional styling (make suggestions gray)
style = Style.from_dict(
    {
        "suggestion": "fg:#4e9a06",
    }
)


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


# --- Intro Animation ---
def matrix_rain(duration=3, width=80, height=24):
    columns = [0] * width
    start_time = time.time()

    # Clear screen once before starting
    # print("\033[2J\033[H", end="")
    os.system("cls" if os.name == "nt" else "clear")

    # Print blank lines to reserve space
    # print("\n" * height)

    while time.time() - start_time < duration:
        print("\033[1;40m", end="")  # Black background
        frame = []

        for y in range(height):
            line = ""
            for i in range(width):
                if random.random() < 0.02:
                    columns[i] = 0
                if columns[i] < y:
                    line += " "
                else:
                    line += f"\033[92m{random.choice(MATRIX_CHARS)}\033[0m"
            frame.append(line)

        print("\n".join(frame))
        columns = [col + 1 for col in columns]
        time.sleep(0.1)

        # Move cursor back to top of animation block
        print(f"\033[{height}A", end="")

    # Clear screen once after animation
    # print("\033[2J\033[H", end="")
    os.system("cls" if os.name == "nt" else "clear")


# --- Typing Effect ---
def type_out_rich(text: Text, delay=0.03):
    styled_chars = text.split()
    for word in styled_chars:
        for char in word.plain:
            # Print each character with the original style
            console.print(
                Text(char, style=word.style), end="", soft_wrap=False, highlight=False
            )
            time.sleep(delay)
        console.print(" ", end="")  # keep word spacing
    print()


def bootstrap():
    init()
    matrix_rain(duration=3)

    type_out_rich(Text("Wake up, Neo...", style="bold green"))
    time.sleep(1)

    type_out_rich(Text("The Matrix has you.", style="bold green"))
    time.sleep(1.5)

    type_out_rich(Text("Follow the white rabbit.", style="bold green"))
    time.sleep(2)

    print()
    print(f"🔵 {Fore.GREEN}Welcome to the Matrix CLI Mode{Fore.GREEN} 🔵")
    print()

    # print(f"{Fore.BLUE}**** Welcome to the assistant bot! ****{Fore.RESET}")
    with data_cxt_mngr() as (book, notes):
        contacts_controller = cntcts_controller(book)
        nts_controller = notes_controller(notes)

        completer = CommandCompleter()

        while True:
            try:
                parts = (
                    prompt("[neo@matrix]$ ", completer=completer, style=style)
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
                        print()
                        print(
                            f"🔴 {Fore.GREEN}Welcome to the Real World{Fore.RESET} 🔴"
                        )
                        print()
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
                    case "help-tree":
                        show_help_ascii_tree()
                    case "test-contacts":
                        run_all_tests()
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
