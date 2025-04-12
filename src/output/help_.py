from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table


def show_help_panels():
    console = Console()

    term_width = console.size.width

    # table_width = 91
    # command_col_width = 46
    # description_col_width = 45

    table_width = term_width // 2 - 1
    command_col_width = table_width // 2
    description_col_width = table_width // 2

    def create_table(title, rows):
        table = Table(
            title=title,
            title_style="bold green",
            header_style="bold white",
            border_style="green",
            box=box.DOUBLE,
            width=table_width,
            style="on black",
        )
        table.add_column(
            "Command",
            style="bold green on black",
            no_wrap=False,
            width=command_col_width,
        )
        table.add_column(
            "Description & Example",
            style="bold green on black",
            width=description_col_width,
        )
        for row in rows:
            table.add_row(*row)
        return table

    contacts_rows = [
        ("contacts add", "📘 Add contact via interactive input"),
        ("contacts add [Field]", "➕ Add field (e.g. phone,email) via prompt"),
        ("contacts add [Name] [Field] [Value]", "📗 Add new contact or update field"),
        ("contacts edit", "   Edit contact via guided prompts"),
        (
            "contacts change [Old_phone] [New_phone]",
            "🔄 Change phone globally in all contacts",
        ),
        ("contacts delete [Name]", "❌ Delete contact"),
        ("contacts remove [Field] [Name]", "   Remove specific field from contact"),
        ("contacts phone [Number]", "📱 Show owner of the phone number"),
        ("contacts all", "📋 Show all contacts"),
        ("contacts add-birthday [Name] [Date]", "🎂 Add birthday to contact"),
        ("contacts show-birthday [Name]", "🎈 Show birthday of the contact"),
        ("contacts birthdays", "📅 Show contacts with upcoming birthdays"),
        ("contacts undo", "   Undo last action"),
    ]

    notes_rows = [
        ("notes create", "📝 Create note via interactive input"),
        ("notes create [Context] [Title] [Tags]", "📗 Create note with full arguments"),
        ("notes edit", "   Edit note via interactive stepper"),
        ("notes edit [ID]", "🆔 Edit note by ID only"),
        ("notes edit [ID] context [Text]", "🧾 Change context of a note"),
        ("notes edit [ID] title [Text]", "📝 Change title of a note"),
        ("notes edit [ID] tags [Old_tags] [New_tags]", "   Replace tags for note"),
        ("notes remove note [ID]", "❌ Remove note by ID"),
        ("notes remove tag [Tags] [Note_id]", "   Remove specific tags from note"),
        ("notes add tags [Tags] [Note_id]", "➕ Add tags to specific note"),
        ("notes find", "🔍 Show all notes"),
        ("notes find [Query]", "🔍 Search notes by id,title,tags,context"),
    ]

    extra_rows = [
        ("help", "[grey37]❓ - display commands list[/grey37]"),
        ("exit | close", "[grey37]🚪 - close the program[/grey37]"),
    ]

    contacts_table = create_table("CONTACTS", contacts_rows)
    notes_table = create_table("NOTES", notes_rows)
    extra_table = create_table("ADDITIONAL COMMANDS", extra_rows)

    header_panel = Panel(
        Align.center("📘 [b]AVAILABLE COMMANDS[/b] 📘", vertical="middle"),
        style="green on black",
        padding=(0, 0),
        width=table_width * 2 + 15,
        box=box.DOUBLE,
    )
    console.print(header_panel)

    left_column = Group(contacts_table, notes_table, extra_table)

    contacts_detail = """
[b green]contacts[/b green]
├── [cyan]create[/cyan] [*name] [*phone] [email, address, birthday]
│   ├── (no args)                     → Start interactive stepper for all fields
│   ├── name [*new_name]
│   ├── phone [*new_phone]
│   ├── email [new_email]
│   ├── birthday [new_birthday]
│   ├── address [address]
│
├── [cyan]edit[/cyan] [*name_of_contact]
│   ├── (no args)                     → Start interactive stepper for all fields
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
└── [cyan]undo[/cyan]                       → Reverts the last add/edit/delete command

[b green]notes[/b green]
├── [cyan]create[/cyan] [*context] [*title] [tags]
│   ├── (no args)                     → Start interactive stepper for all fields
│   ├── context
│   ├── title
│   └── tags # example: tag1,tag2,tag3
│
├── [cyan]edit[/cyan] [*id] | [field_name] -> [*context] [*title] [tags] 
│   ├── (no args)                     → Start interactive stepper for all fields
│   ├── id # provided by user
│   ├── context
│   ├── title
│   └── tags: [*old_tags] [*new_tags] # example: tag1,tag2,tag3
│
├── [cyan]remove[/cyan] [*note_id] # remove note 1, remove ID1 tag tag1,tag2
│   ├── tag [*tags]
│   └── note [*id]
│
├── [cyan]add tags[/cyan] [*tags: tag1,tag2] [*note_id]
│
└── [cyan]find[/cyan] [*query] # default all
    ├── id
    ├── title
    ├── tag/tags
    └── context
"""
    right_panel = Panel(
        contacts_detail,
        title="📂 CONTACTS COMMAND TREE",
        border_style="green",
        box=box.DOUBLE,
        padding=(1, 2),
        width=table_width,
        height=63,
        style="on black",
    )

    layout = Columns([left_column, right_panel], padding=3)
    console.print(layout)

    choice_panel = Panel(
        Align.center(
            "[bold green]💊 Which pill will you choose? 🔴 | 🔵[/bold green]",
            vertical="middle",
        ),
        border_style="green",
        title="THE MATRIX",
        title_align="center",
        box=box.DOUBLE,
        style="on black",
        padding=(0, 1),
        width=table_width * 2 + 15,
    )
    console.print(choice_panel)


if __name__ == "__main__":
    show_help_panels()
