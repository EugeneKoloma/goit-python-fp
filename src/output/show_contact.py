from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def get_ascii_photo() -> str:
    return r"""
     _______
    /       \
   |  .-. .-. |
   |  |_| |_| |
   |  \___/  |
    \_______/
    """


def show_contact_card(record):
    ascii_photo = get_ascii_photo()

    # 1. PHOTO PANEL
    photo_panel = Panel.fit(
        ascii_photo,
        border_style="blue",
        box=box.ROUNDED,
        padding=(0, 1),
        title="Photo",
        title_align="left",
    )

    # 2. CONTACT INFO with interlaced row styles and padding between rows
    contact_table = Table.grid(padding=(1, 1), expand=True)
    contact_table.add_column(justify="left", style="bold cyan", no_wrap=True)
    contact_table.add_column(style="white")

    # Optional: define alternating row styles (backgrounds)
    contact_table.row_styles = ["", "on #1c1c1c"]

    def add_if_exists(label, value):
        if value:
            contact_table.add_row(f"{label}:", str(value))

    add_if_exists("Name", record.name)
    for phone in record.phones:
        add_if_exists("Phone", phone)
    for email in getattr(record, "emails", []):
        add_if_exists("Email", email)
    add_if_exists("Birthday", getattr(record, "birthday", None))
    add_if_exists("Address", getattr(record, "address", None))
    if hasattr(record, "tags") and record.tags:
        tags = " ".join([f"#{str(tag)}" for tag in record.tags])
        add_if_exists("Tags", tags)

    # 3. INNER layout table: photo on left, contact details on right
    content = Table.grid(padding=0)
    content.add_column(ratio=1)
    content.add_column(ratio=3)
    content.add_row(photo_panel, contact_table)

    # 4. OUTER card with vertical centering
    term_width, term_height = console.size
    max_width = term_width // 2

    card_panel = Panel.fit(
        Align.left(content, vertical="middle"),
        title=f"📇 Contact {record.name} Details",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2),
        width=max_width,
    )

    console.print(Align.left(card_panel, vertical="middle"))
