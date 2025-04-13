from rich import box
from rich.align import Align
from rich.ansi import AnsiDecoder
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

console = Console()

DEFAULT_ASCII = "photo/nophoto.txt"


def fallback_print_ansi(ascii_art: str):
    console = Console()
    decoder = AnsiDecoder()
    segments = list(decoder.decode(ascii_art))
    group = Group(*segments)
    console.print(group)


def get_ascii_photo(record):
    if getattr(record, "photo", None):
        path = record.photo.value.strip()
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()  # ← DO NOT strip ANSI
        except Exception as e:
            return f"[Error reading file: {e}]"
    else:
        path = DEFAULT_ASCII
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()  # ← DO NOT strip ANSI
        except Exception as e:
            return f"[Error reading file: {e}]"


def show_contact_card(record):
    # 1. Get and render color ASCII photo with raw ANSI
    ascii_art = get_ascii_photo(record)
    fallback_print_ansi(ascii_art)  # <-- best quality rendering!

    # 2. Build contact info table (right-aligned)
    contact_table = Table.grid(padding=(0, 1))
    contact_table.add_column(justify="right", style="bold cyan")
    contact_table.add_column()

    def add(label, value):
        if value:
            contact_table.add_row(f"{label}:", str(value))

    add("Name", record.name)
    for phone in record.phones:
        add("Phone", phone)
    for email in getattr(record, "emails", []):
        add("Email", email)
    add("Birthday", getattr(record, "birthday", None))
    add("Address", getattr(record, "address", None))
    if getattr(record, "tags", None):
        tags = " ".join(f"{str(tag)}" for tag in record.tags)
        add("Tags", tags)

    # 3. Wrap the contact card in a styled panel
    term_width = console.size.width
    max_width = term_width // 2

    contact_panel = Panel(
        Align.center(contact_table),
        title=f"📇 Contact {record.name} Details",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2),
        width=max_width,
    )

    console.print(contact_panel)
