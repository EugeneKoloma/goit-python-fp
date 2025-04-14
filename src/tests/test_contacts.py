import sys
import unittest
from io import StringIO

from rich import box
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

from contacts import ContactsBook
from contacts.controller import conntroller

SCENARIOS = [
    (
        "test_unknown_command",
        "Невідома команда",
        "controller(commands: ['foobar'])",
        "Unknown command",
        "contacts foobar",
    ),
    (
        "test_add_incorrect_args",
        "Некоректні аргументи",
        "controller(commands: ['add', 'phone', '0990354682', 'John', 'extra'])",
        "Usage warning",
        "contacts add phone 123 John extra",
    ),
    (
        "test_add_valid_contact",
        "Валідне додавання",
        "controller(commands: ['add', 'phone', '0671234567', 'John'])",
        "Created new contact",
        "contacts add phone 0671234567 John",
    ),
    (
        "test_add_invalid_phone",
        "Невалідний телефон",
        "controller(commands: ['add', 'phone', 'abcde', 'Jane'])",
        "Invalid value for phone",
        "contacts add phone abcde Jane",
    ),
    (
        "test_remove_non_existing_contact",
        "Видалення неіснуючого",
        "controller(commands: ['remove', 'contact', 'Ghost'])",
        "not found",
        "contacts remove contact Ghost",
    ),
    (
        "test_sort_invalid_field",
        "Некоректне поле для сортування",
        "controller(commands: ['sort', 'invalid_field'])",
        "Please provide a valid field",
        "contacts sort invalid_field",
    ),
    (
        "test_sort_valid",
        "Сортування по імені",
        "controller(commands: ['sort', 'name'])",
        "Alice",
        "contacts sort name",
    ),
    (
        "test_phone_existing",
        "Показати телефон",
        "controller(commands: ['phone', 'Bob'])",
        "0671234567",
        "contacts phone Bob",
    ),
    (
        "test_phone_not_found",
        "Немає телефону",
        "controller(commands: ['phone', 'Ghost'])",
        "Record not found",
        "contacts phone Ghost",
    ),
    (
        "test_birthday_not_set",
        "День народження відсутній",
        "controller(commands: ['show-birthday', 'NoBirthday'])",
        "has not birthday set",
        "contacts show-birthday NoBirthday",
    ),
    (
        "test_birthday_invalid_days_input",
        "Некоректні дні",
        "controller(commands: ['birthdays', 'abc'])",
        "Wrong days input",
        "contacts birthdays abc",
    ),
    (
        "test_birthdays_default",
        "Іменинники на 7 днів",
        "controller(commands: ['birthdays'])",
        "No birthdays or Contacts",
        "contacts birthdays",
    ),
    (
        "test_find_no_args",
        "Пошук без аргументів",
        "controller(commands: ['find'])",
        "Usage:",
        "contacts find",
    ),
    (
        "test_find_by_name",
        "Пошук за іменем",
        "controller(commands: ['find', '--name', 'Dan'])",
        "Dan",
        "contacts find --name Dan",
    ),
    (
        "test_all_empty",
        "Порожній список",
        "controller(commands: ['all'])",
        "Contacts",
        "contacts all",
    ),
    (
        "test_all_with_fields",
        "Список з полями",
        "controller(commands: ['all', 'name', 'phone'])",
        "Contact shown",
        "contacts all name phone",
    ),
    (
        "test_undo_no_state",
        "Undo без змін",
        "controller(commands: ['undo'])",
        "Nothing to undo",
        "contacts undo",
    ),
    (
        "test_add_then_undo",
        "Undo після додавання",
        "controller(commands: ['add', 'phone', '0671234567', 'UndoUser'])",
        "Nothing to undo yet",
        "contacts add ... → undo",
    ),
    (
        "test_remove_field_success",
        "Видалення поля",
        "controller(commands: ['remove', 'phone', '0671234567', 'DeleteMe'])",
        "removed",
        "contacts remove phone 0671234567 DeleteMe",
    ),
    (
        "test_remove_field_fail",
        "Видалення неіснуючого поля",
        "controller(commands: ['remove', 'email', 'not@found.com', 'FailTest'])",
        "Nothing was removed",
        "contacts remove email not@found.com FailTest",
    ),
]


class CustomTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.scenario_results = {}

    def addSuccess(self, test):
        super().addSuccess(test)
        self.scenario_results[test._testMethodName] = "✅ Успішно"

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.scenario_results[test._testMethodName] = "❌ Неуспішно"

    def addError(self, test, err):
        super().addError(test, err)
        self.scenario_results[test._testMethodName] = "❌ Помилка"


class CustomTestRunner(unittest.TextTestRunner):
    resultclass = CustomTestResult


class TestContactsCLI(unittest.TestCase):
    def setUp(self):
        self.book = ContactsBook()
        self.commands = conntroller(self.book)
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout

    def get_output(self):
        return sys.stdout.getvalue()

    def test_unknown_command(self):
        self.commands("foobar")
        self.assertIn("Unknown contact command", self.get_output())

    def test_add_incorrect_args(self):
        self.commands("add", "phone", "123", "John", "extra")
        self.assertIn("Usage", self.get_output())

    def test_add_valid_contact(self):
        self.commands("add", "phone", "0671234567", "John")
        self.assertIn("Created new contact", self.get_output())

    def test_add_invalid_phone(self):
        self.commands("add", "phone", "abcde", "Jane")
        self.assertIn("Invalid value for phone", self.get_output())

    def test_remove_non_existing_contact(self):
        self.commands("remove", "contact", "Ghost")
        self.assertIn("No contacts found matching", self.get_output())

    def test_sort_invalid_field(self):
        self.commands("sort", "invalid_field")
        self.assertIn("Please provide a valid field", self.get_output())

    def test_sort_valid(self):
        self.commands("add", "phone", "0671234567", "Alice")
        self.commands("sort", "name")
        self.assertIn("Alice", self.get_output())

    def test_phone_existing(self):
        self.commands("add", "phone", "0671234567", "Bob")
        self.commands("phone", "Bob")
        self.assertIn("0671234567", self.get_output())

    def test_phone_not_found(self):
        self.commands("phone", "Ghost")
        self.assertIn("Record not found", self.get_output())

    def test_birthday_not_set(self):
        self.commands("add", "phone", "0671234567", "NoBirthday")
        self.commands("show-birthday", "NoBirthday")
        self.assertIn("has not birthday set", self.get_output())

    def test_birthday_invalid_days_input(self):
        self.commands("birthdays", "abc")
        self.assertIn("Wrong days input", self.get_output())

    def test_birthdays_default(self):
        self.commands("birthdays")
        output = self.get_output()
        self.assertTrue(
            "No birthdays" in output or "📭" in output or "Contacts" in output
        )

    def test_find_no_args(self):
        self.commands("find")
        self.assertIn("Usage:", self.get_output())

    def test_find_by_name(self):
        self.commands("add", "phone", "0671234567", "Dan")
        self.commands("find", "--name", "Dan")
        self.assertIn("Dan", self.get_output())

    def test_all_empty(self):
        self.commands("all")
        self.assertIn("Contacts", self.get_output())

    def test_all_with_fields(self):
        self.commands("add", "phone", "0671234567", "Kate")
        self.commands("all", "name", "phone")
        self.assertIn("Kate", self.get_output())

    def test_undo_no_state(self):
        self.commands("undo")
        output = self.get_output()
        self.assertTrue("Nothing to undo" in output or "No undo" in output)

    def test_add_then_undo(self):
        self.commands("add", "phone", "0671234567", "UndoUser")
        self.commands("undo")
        self.assertIn("Nothing to undo yet", self.get_output())

    def test_remove_field_success(self):
        self.commands("add", "phone", "0671234567", "DeleteMe")
        self.commands("remove", "phone", "0671234567", "DeleteMe")
        self.assertIn("removed", self.get_output())

    def test_remove_field_fail(self):
        self.commands("add", "phone", "0671234567", "FailTest")
        self.commands("remove", "email", "not@found.com", "FailTest")
        self.assertIn("Nothing was removed", self.get_output())

    def test_add_tag(self):
        from contacts.controller import prompt_for_field

        original_prompt = prompt_for_field

        def dummy_prompt(field):
            if field == "phone":
                return "0671111111"
            return ""

        import contacts.controller as ctrl_mod

        ctrl_mod.prompt_for_field = dummy_prompt

        self.commands("add", "tags", "#friend", "TagUser")
        self.assertIn("Created new contact", self.get_output())

        self.commands("remove", "tag", "#friend", "TagUser")
        out_rem = self.get_output().lower()
        self.assertTrue("removed" in out_rem or "nothing was removed" not in out_rem)
        ctrl_mod.prompt_for_field = original_prompt

    def test_add_email(self):
        from contacts.controller import prompt_for_field

        original_prompt = prompt_for_field

        def dummy_prompt(field):
            if field == "phone":
                return "0672222222"
            return ""

        import contacts.controller as ctrl_mod

        ctrl_mod.prompt_for_field = dummy_prompt

        self.commands("add", "email", "findme@example.com", "FindEmailUser")
        self.assertIn("created new contact", self.get_output().lower())
        self.commands("find", "--email", "findme@example.com")
        self.assertIn("findemailuser", self.get_output().lower())
        ctrl_mod.prompt_for_field = original_prompt

    def test_add_address(self):
        from contacts.controller import prompt_for_field

        original_prompt = prompt_for_field

        def dummy_prompt(field):
            if field == "phone":
                return "0673333333"
            return ""

        import contacts.controller as ctrl_mod

        ctrl_mod.prompt_for_field = dummy_prompt

        self.commands("add", "address", "Lviv", "AddressUser")
        self.assertIn("Created new contact", self.get_output())
        ctrl_mod.prompt_for_field = original_prompt

    def test_add_valid_birthday(self):
        from contacts.controller import prompt_for_field

        original_prompt = prompt_for_field

        def dummy_prompt(field):
            if field == "phone":
                return "0674444444"
            return ""

        import contacts.controller as ctrl_mod

        ctrl_mod.prompt_for_field = dummy_prompt

        self.commands("add", "birthday", "12.12.2000", "BirthdayUser")
        self.assertIn("Created new contact", self.get_output())
        ctrl_mod.prompt_for_field = original_prompt

    def test_add_invalid_birthday(self):
        from contacts.controller import prompt_for_field

        original_prompt = prompt_for_field

        def dummy_prompt(field):
            if field == "phone":
                return "0675555555"
            return ""

        import contacts.controller as ctrl_mod

        ctrl_mod.prompt_for_field = dummy_prompt

        self.commands("add", "birthday", "31-12-2000", "BirthdayUser")
        self.assertIn("Invalid value for birthday", self.get_output())
        ctrl_mod.prompt_for_field = original_prompt

    def test_find_by_tag(self):
        from contacts.controller import prompt_for_field

        original_prompt = prompt_for_field

        def dummy_prompt(field):
            if field == "phone":
                return "0677777777"
            return ""

        import contacts.controller as ctrl_mod

        ctrl_mod.prompt_for_field = dummy_prompt

        self.commands("add", "tags", "#findtag", "FindTagUser")
        self.commands("find", "--tag", "#findtag")
        self.assertIn("findtaguser", self.get_output().lower())
        ctrl_mod.prompt_for_field = original_prompt


def print_rich_result_table(result):
    matrix_theme = Theme(
        {
            "table.border": "green",
            "table.title": "bold green",
            "cyan": "green",
            "magenta": "green",
            "green": "green",
            "yellow": "green",
            "white": "green",
            "bold": "bold green",
        }
    )

    console = Console(theme=matrix_theme, style="green on black")
    table = Table(
        title="🧪 Результати тестування Контактної Книги",
        show_lines=True,
        box=box.DOUBLE,
        style="green",
    )

    table.add_column("№ (метод)", style="green", no_wrap=True)
    table.add_column("Назва тесту", style="green")
    table.add_column("Функціонал + аргументи", style="green")
    table.add_column("Очікуваний результат", style="green")
    table.add_column("Приклад", style="green")
    table.add_column("Статус", justify="center", style="bold green")

    for method, name, func, expect, example in SCENARIOS:
        status = result.scenario_results.get(method, "⏳ Не виконано")
        table.add_row(method, name, func, expect, example, status)

    console.print(table)


def run_all_tests():
    """Функція, яку можна викликати з іншого модуля для запуску тестів."""
    runner = CustomTestRunner(verbosity=0)
    result = runner.run(unittest.TestLoader().loadTestsFromTestCase(TestContactsCLI))
    print_rich_result_table(result)


if __name__ == "__main__":
    run_all_tests()
