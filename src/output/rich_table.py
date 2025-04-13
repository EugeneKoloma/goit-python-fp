from rich import box
from rich.console import Console
from rich.table import Table

console = Console()
# Change colors later
default_contacts_table_fields = [
    "Name",
    "Phones",
    "Birthday",
    "Emails",
    "Address",
    "Tags"
]

def display_notes_table(records):
    """
    Takes a list of `Record` objects and prints them in a formatted table.
    Each record is expected to have:
      - title (record.title.value)
      - context (record.context.value)
      - updated_at (record.date.value)
      - tags (record.tags)
    """

    # Change colors later
    table = Table(
        title="Notes",
        show_lines=False,
        box=box.ROUNDED,
        header_style="bold white",
        row_styles=["on #1a1a1a", "on #2a2a2a"],
    )
    table.add_column("Title", style="bold cyan")
    table.add_column("Context", style="green", width=40)
    table.add_column("Date", style="magenta")
    table.add_column("Tags", style="red")

    # Get Record attributes
    for record in records:
        title = str(record.title)

        context = str(record.context) if record.context else "—"

        date = str(record.updated_at) if record.updated_at else "—"

        tags = getattr(record, "tags", [])
        tags = ", ".join([str(tag) for tag in tags]) if tags else "—"

        table.add_row(title.capitalize(), context, date, tags)

    console.print(table)


# To display contacts as rich table
def display_contacts_table(records, user_fields: list = []):
    """
    Takes a list of `Record` objects and prints them in a formatted table.
    Each record is expected to have:
      - name (record.name.value)
      - phones (list of record.phones)
      - birthday (record.birthday)
      - email (record.email)
      - address (record.address)
      - tags (record.tags)
    """
    
    table = Table(
        title="Contacts",
        show_lines=False,
        header_style="bold white",
        row_styles=["on black", "on grey11"],
        box=box.ROUNDED,
    )
    table.add_column("Name", style="bold cyan", max_width=12)
    table.add_column("Phones", style="green", max_width=12)
    table.add_column("Birthday", style="magenta", max_width=12)
    table.add_column("Emails", style="yellow", max_width=20)
    table.add_column("Address", style="yellow", max_width=25)
    table.add_column("Tags", style="red", max_width=12)

    # Get Record attributes
    for record in records:
        name = str(record.name)

        phones = getattr(record, "phones", None)
        phones = " ".join([p.value for p in record.phones]) if record.phones else "—"

        birthday = str(record.birthday) if record.birthday else "—"

        emails = getattr(record, "emails", None)
        emails = (
            ", ".join([e.value for e in record.emails])
            if hasattr(record, "emails") and record.emails
            else "—"
        )

        address = (
            str(record.address)
            if hasattr(record, "address") and record.address
            else "—"
        )

        tags = getattr(record, "tags", None)
        tags = ", ".join(tags) if tags else "—"

        table.add_row(
            name.capitalize(), phones, birthday, emails, address, tags
        )  # <- Add email and address inside later and wrap like tags, the same way

    global default_contacts_table_fields
    if user_fields:
        # Make a list of indexes of fields, that are not in user's choice
        indexes = []
        index = 0
        for field in default_contacts_table_fields:
            if field not in user_fields:
                indexes.append(index)
            index += 1

        # Removing the fields, which a not in user's choice, by their index
        while indexes:
            table.columns.pop(indexes[0])
            for i in range(len(indexes)):
                indexes[i] -= 1
            indexes.remove(indexes[0])

    console.print(table)


# To display birthdays as rich table
def display_birthdays_table(birthdays, days_to):
    """
    Takes a list of dicts with keys: name, congratulation_date, days_to_user_congrats,
    and displays them as a rich table.
    """
    table = Table(
        title=f"Birthdays in the Next {days_to} Days",
        show_lines=False,
        header_style="bold white",
        row_styles=["on black", "on grey11"],
        box=box.ROUNDED,
    )
    table.add_column("Name", style="cyan", justify="center")
    table.add_column("Date", style="green", justify="center")
    table.add_column("Days Left", style="yellow", justify="center")

    for entry in birthdays:
        table.add_row(
            entry["name"].capitalize(),
            entry["congratulation_date"],
            str(entry["days_to_user_congrats"]),
        )

    console.print(table)
