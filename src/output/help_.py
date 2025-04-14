import re

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def highlight_args(text: str) -> str:
    # Підсвічує все в квадратних дужках
    return re.sub(r"(\[[^\]]+\])", r"[cyan]\1[/cyan]", text)


def show_help_panels():
    console = Console()
    term_width = console.size.width
    panel_width = term_width - 4
    column_width = panel_width // 3

    def create_table(title, rows):
        table = Table(
            title=title,
            title_style="bold green",
            header_style="bold green on black",
            border_style="green",
            box=box.DOUBLE,
            style="on black",
            width=panel_width,
        )
        table.add_column(
            "Command [Args]", style="green on black", width=column_width, no_wrap=False
        )
        table.add_column(
            "Description", style="green on black", width=column_width, no_wrap=False
        )
        table.add_column(
            "Example", style="green on black", width=column_width, no_wrap=False
        )
        for row in rows:
            command, description, example = row
            table.add_row(highlight_args(command), description, highlight_args(example))
        return table

    contacts_rows = [
        ("contacts add", "Interactive contact creation", "contacts add"),
        ("contacts add [Field]", "Add one field via prompt", "contacts add phone"),
        (
            "contacts add [Name] [Field] [Value]",
            "Quick add or update",
            "contacts add John phone 1234567",
        ),
        ("contacts edit", "Edit contact via prompt", "contacts edit"),
        (
            "contacts change [Old_phone] [New_phone]",
            "Change phone globally",
            "contacts change 1234567 7654321",
        ),
        (
            "contacts remove contact [Name]",
            "Delete full contact",
            "contacts remove contact John",
        ),
        (
            "contacts remove [Field] [Value] [Name]",
            "Remove specific field",
            "contacts remove email john@email.com John",
        ),
        ("contacts phone [Number]", "Find contact by phone", "contacts phone 1234567"),
        ("contacts all", "Show all contacts", "contacts all"),
        (
            "contacts add-birthday [Name] [Date]",
            "Add birthday",
            "contacts add-birthday John 01.01.2000",
        ),
        (
            "contacts show-birthday [Name]",
            "Show contact's birthday",
            "contacts show-birthday John",
        ),
        (
            "contacts birthdays [N Next Days]",
            "Upcoming birthdays list in next N days",
            "contacts birthdays 10",
        ),
        ("contacts undo", "Undo last action", "contacts undo"),
        (
            "contacts sort [Field] [asc|desc]",
            "Sort contacts",
            "contacts sort name desc",
        ),
        (
            "contacts find [--name] [--phone] ...",
            "Search by fields or keyword",
            "contacts find --tag work",
        ),
        (
            "contacts export [file.csv]",
            "Export contacts to CSV",
            "contacts export backup.csv",
        ),
        (
            "contacts import [file.csv]",
            "Import contacts from CSV",
            "contacts import backup.csv",
        ),
    ]

    notes_rows = [
        (
            "notes create\n   Title [Title (opt)]\n   Context [*Context]\n   Tags [Tags (opt)]",
            "Create note via step by step input",
            "notes create\n   Some title\n   Some context\n   Some tags",
        ),
        (
            "notes create [Context]",
            "Create note by it's context with tags by '#'",
            'notes create "Some default note with tags #milk and #way."',
        ),
        (
            "notes edit\n   ID [ID]\n   prompt [Title | Context | Tags]",
            "Edit note via prompt",
            "notes edit\n   1\n   title: new title",
        ),
        (
            "notes edit [ID] title [Text]",
            "Edit title of note",
            "notes edit 1 title Meeting",
        ),
        (
            "notes edit [ID] context [Text]",
            "Edit context of note",
            "notes edit 1 context 'Updated context'",
        ),
        (
            "notes edit [ID] tags [Old] [New]",
            "Replace tags",
            "notes edit 1 tags oldtag newtag",
        ),
        ("notes remove note [ID]", "Delete note by ID", "notes remove note 1"),
        (
            "notes remove tag [NoteID] [Tags]",
            "Remove tags from note",
            "notes remove tag 1 tag1,tag2",
        ),
        (
            "notes add-tags [Tags] [NoteID]",
            "Add tags to note",
            "notes add tags tag1,tag2 1",
        ),
        ("notes find [Query]", "Search notes smartly", "notes find shopping"),
        ("notes find id [NoteID]", "Find note by ID", "notes find id 1"),
        ("notes find title [Text]", "Find notes by title", "notes find title Meeting"),
        (
            "notes find context [Text]",
            "Find notes by context",
            "notes find context work",
        ),
        (
            "notes find tag [Tags]",
            "Find notes by tags",
            "notes find tag urgent,home",
        ),
        ("notes all", "Show all notes", "notes all"),
        ("notes export [File-name (def. .\\data\\contacts.csv)]", "Export notes to CSV", "notes export backup.csv"),
    ]

    extra_rows = [
        ("help", "Display help menu", "help"),
        ("help-tree", "Display help command-tree", "help-tree"),
        ("test-contacts", "Run test", "Result of test"),
        ("exit | close", "Close the program", "exit"),
    ]

    contacts_table = create_table("CONTACTS", contacts_rows)
    notes_table = create_table("NOTES", notes_rows)
    extra_table = create_table("ADDITIONAL COMMANDS", extra_rows)

    header_panel = Panel(
        Align.center("[b]AVAILABLE COMMANDS[/b]", vertical="middle"),
        style="green on black",
        box=box.DOUBLE,
        width=panel_width,
        padding=(0, 1),
    )

    choice_panel = Panel(
        Align.center(
            "[bold green]💊 Which pill will you choose? 🔴 | 🔵[/bold green]",
            vertical="middle",
        ),
        border_style="green",
        title="THE MATRIX",
        title_align="center",
        box=box.DOUBLE,
        style="green on black",
        width=panel_width,
        padding=(0, 1),
    )

    console.print(header_panel)
    console.print(contacts_table)
    console.print(notes_table)
    console.print(extra_table)
    console.print(choice_panel)


def show_help_ascii_tree():
    console = Console()

    tree_text = """[bold green]
contacts
├── [cyan]add[/cyan] [*name] [*phone] [email, address, birthday]
│   ├── (no args)                  [grey50]→ Start interactive stepper for all fields[/grey50]
│   ├── name [*new_name]
│   ├── phone [*new_phone]
│   ├── email [new_email]
│   ├── birthday [new_birthday]
│   └── address [address]
│
├── [cyan]edit[/cyan] [*name_of_contact]
│   ├── (no args)                     [grey50]→ Start interactive stepper for all fields[/grey50]
│   ├── name [*new_name]
│   ├── phone [*old_phone] [*new_phone]
│   ├── email [*old_email] [*new_email]
│   ├── birthday [*new_birthday]
│   ├── address [*new_address]
│   └── tag [*old_tag] [*new_tag]
│
├── [cyan]add[/cyan] [field: phone | email | tag] [*value] [*name_of_contact]
│   ├── phone [*value]
│   ├── email [*value]
│   └── tag [*value]
│
├── [cyan]remove[/cyan] [type: contact | phone | email | tag] [*value] [*name_of_contact]
│   ├── contact [*name_of_contact]
│   ├── phone [*value]
│   ├── email [*value]
│   └── tag [*value]
│
├── [cyan]find[/cyan] [*query]
├── [cyan]show birthdays[/cyan] [*n-days-forward]
└── [cyan]undo[/cyan]                       [grey50]→ Reverts the last add/edit/delete command[/grey50]

[bold green]
notes
├── [cyan]create[/cyan] [*context] [*title] [tags]
│   ├── (no args)                     [grey50]→ Start interactive stepper for all fields[/grey50]
│   ├── context
│   ├── title
│   └── tags                        [grey50]# example: tag1,tag2,tag3[/grey50]
│
├── [cyan]edit[/cyan] [*id] | [field_name] → [*context] [*title] [tags]
│   ├── (no args)                     [grey50]→ Start interactive stepper for all fields[/grey50]
│   ├── id                           [grey50]# provided by user[/grey50]
│   ├── context
│   ├── title
│   └── tags: [*old_tags] [*new_tags]   [grey50]# example: tag1,tag2,tag3[/grey50]
│
├── [cyan]remove[/cyan] [*note_id]       [grey50]# remove note 1, remove ID1 tag tag1,tag2[/grey50]
│   ├── tag [*tags]
│   └── note [*id]
│
├── [cyan]add-tags[/cyan] [*tags: tag1,tag2] [*note_id]
│
└── [cyan]find[/cyan] [*query]          [grey50]# default all[/grey50]
    ├── id
    ├── title
    ├── tag/tags
    └── context
[/bold green]"""

    panel = Panel.fit(
        tree_text,
        title="[b]COMMAND STRUCTURE[/b]",
        title_align="left",
        border_style="green",
        box=box.DOUBLE,
        style="on black",
    )

    console.print(panel)


# if __name__ == "__main__":
#   show_help_panels()
