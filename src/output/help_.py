from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel


def show_help_panels():
    console = Console()

    contacts_text = """
    📞 [cyan]add [green][Name] [Phone Number][/green][/cyan] [white]- create new record[/white]
    [cyan]change [green][Name] [New Phone Number][/green][/cyan] [white]- change phone number by [Name][/white]
    [cyan]phone [green][Phone Number][/green][/cyan] [white]- display owner name[/white]
    [cyan]all[/cyan] [white]- list all users with their number[/white]
    [cyan]add-birthday [green][Name] [DD.MM.YYYY][/green][/cyan] [white]- add to provided contact its birthday[/white]
    [cyan]show-birthday [green][Name][/green][/cyan] [white]- display contacts birthday[/white]
    [cyan]birthdays[/cyan] [white]- show contacts which have birthdays in next 7 days[/white]
    """

    notes_text = """
    for example:

    [cyan]add-note ----------------------------------------[/cyan]
    [cyan]edit-note 
    [cyan]delete-note 
    [cyan]search-notes 
    """

    extra_text = """
    ❓ [cyan]help[/cyan] [white]- display commands list
    🚪 [cyan]exit | close[/cyan] [white]- close the program
    """

    panel_height = 11

    header_panel = Panel(
        Align.center("📘 [b]AVAILABLE COMMANDS[/b] 📘", vertical="middle"),
        style="green on black",
        padding=(0, 71),
        expand=False,
        box=box.DOUBLE,
    )

    contact_panel = Panel(
        contacts_text,
        title="📇 [b]CONTACTS[/b]",
        border_style="green",
        height=panel_height,
        style="green on black",
    )
    notes_panel = Panel(
        notes_text,
        title="📝 [b]NOTES[/b]",
        border_style="blue",
        height=panel_height,
        style="green on black",
    )
    extra_panel = Panel(
        extra_text,
        title="⚙️  [b]ADDITIONAL COMMANDS[/b]",
        border_style="magenta",
        height=panel_height,
        style="green on black",
    )

    console.print(header_panel)
    console.print(Columns([contact_panel, notes_panel, extra_panel]))
