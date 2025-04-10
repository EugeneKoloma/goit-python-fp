from rich.console import Console
from rich.table import Table

console = Console()


# To display contacts as rich table
def display_contacts_table(records):
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

    # Change colors later
    table = Table(title="Contacts", show_lines=True, header_style="bold white")
    table.add_column("Name", style="bold cyan")
    table.add_column("Phone Numbers", style="green")
    table.add_column("Birthday", style="magenta")
    table.add_column("Emails", style="yellow")
    table.add_column("Address", style="yellow")
    table.add_column("Tags", style="red")

    # Get Record attributes
    for record in records:
        name = str(record.name)

        phones = getattr(record, "phones", None)
        phones = ", ".join([p.value for p in record.phones]) if record.phones else "—"

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

    console.print(table)


# To display birthdays as rich table
def display_birthdays_table(birthdays, days_to):
    """
    Takes a list of dicts with keys: name, congratulation_date, days_to_user_congrats,
    and displays them as a rich table.
    """
    table = Table(
        title=f"Birthdays in the Next {days_to} Days",
        show_lines=True,
        header_style="bold magenta",
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
