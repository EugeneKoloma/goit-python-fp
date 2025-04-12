"""
Updated outpot module
=====================

All messages now outputs using rich
and are quite flexibly configurable
"""

import re

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

"""
ANSI cleaner function - temporary, before (if?) we remove all colorama
Without it rich draws borders incorrectly
"""


def strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")  # Removes colorama injections
    return ansi_escape.sub("", text)


def output_info(message: str):
    # Clean the message of all garbage
    clean = strip_ansi(message.strip().replace("\n", " ").replace("\r", ""))
    text = Text(clean, style="white")
    panel = Panel.fit(
        text,
        title="INFO",  # puts title text
        title_align="left",  # or "center" / "right"
        border_style="green",  # sets borders color
        box=box.SQUARE,  # sets borders style
        padding=(0, 1),  # add space (top/bottom, left/right)
    )
    console.print(panel)


def output_warning(message: str):
    clean = strip_ansi(message.strip().replace("\n", " ").replace("\r", ""))
    text = Text(clean, style="white")
    panel = Panel.fit(
        text,
        title="WARNING",
        title_align="left",
        border_style="yellow",
        box=box.SQUARE,
        padding=(0, 1),
    )
    console.print(panel)


def output_error(message: str):
    clean = strip_ansi(message.strip().replace("\n", " ").replace("\r", ""))
    text = Text(clean, style="white")
    panel = Panel.fit(
        text,
        title="ERROR",
        title_align="left",
        border_style="red",
        box=box.SQUARE,
        padding=(0, 1),
    )
    console.print(panel)


def notes_output(notes: dict):        
    for id, note in notes.items():  
        tags = " ".join([str(tag) for tag in note.tags]) + "\n" if note.tags else ""
        panel = Panel(
            f"{note.context.value}\n" 
            + f"[bold cyan]{tags}[/bold cyan]"
            + f"[yellow]     Created at | {note.created_at}\nLast updated at | {note.updated_at}[/yellow]", 
            title=f"[bold magenta]📝 ID{id}[/bold magenta] [bold cyan]| {note.title.value} |[/bold cyan]",
            title_align="left",
            style="white on black",
            padding=(0, 1),
            border_style="green",
            expand=False,
            box=box.DOUBLE,
            width=100,            
        )
        console.print(panel) 
        console.print() 

if __name__ == "__main__":
    output_info("This is an info message.")
    output_error("This is an error message.")
    output_warning("This is a warning message.")
