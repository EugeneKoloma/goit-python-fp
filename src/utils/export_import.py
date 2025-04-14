import re
import csv
from pathlib import Path

from output import default_contacts_table_fields
from decorators import error_handler
from exceptions import WrongFileName
from output import output_error, output_info

from contacts.ContactsBook import ContactsBook
from contacts.Records import Record
from notes import Notes


@error_handler
def export_contacts_to_csv(book: ContactsBook, args: list = ["./data/contacts.csv"]):    
    file_name, *fields = args
    file_name = file_name.lower().strip()
    folder = file_name.split("/")[:-1]
    if not file_name.endswith(".csv"):
        raise WrongFileName
    
    folder = Path("".join(folder))
    file_name = Path(file_name)
    folder.mkdir(parents=True, exist_ok=True)


    if not book:
        output_info(f"Export to '{file_name}' impossible. ContactsBook is empty yet!")
        return

    if not fields:
        fields = default_contacts_table_fields
    else:
        fields = [
            field
            for field in default_contacts_table_fields
            if field.lower() in fields
        ]

        # removing duplicates, if exist
        fields = set(fields)
        if "Name" not in fields:
            fields.add("Name")

    try:
        with open(file_name, "w+", newline="", encoding="UTF-8") as file:  
            writer = csv.writer(file, delimiter=",")
            writer.writerow(fields)
            for record in book.data.values():
                name = str(record.name)

                phones = getattr(record, "phones", None)
                phones = ";".join([p.value for p in record.phones]) if record.phones else "—"

                birthday = str(record.birthday) if record.birthday else "—"

                emails = getattr(record, "emails", None)
                emails = (
                    ";".join([e.value for e in record.emails])
                    if hasattr(record, "emails") and record.emails
                    else "—"
                )

                address = (
                    f"({str(record.address)})"
                    if hasattr(record, "address") and record.address
                    else "—"
                )

                tags = getattr(record, "tags", None)
                tags = ";".join(tags) if tags else "—"

                photo = getattr(record, "photo", None)
                photo = f"{photo.value}" if photo else "—"

                whole_data = {
                    "Name": name,
                    "Phones": phones,
                    "Birthday": birthday,
                    "Emails": emails,
                    "Address": address,
                    "Tags": tags,
                    "Photo": photo,
                }

                csv_row = [
                    data
                    for field, data in whole_data.items()
                    if field in fields
                ]
                writer.writerow(csv_row)

        output_info(f"Export to '{file_name}' successful!")

    except OSError:
        output_error(f"Name of '{file_name}' file contains invalid argument! Please, give me a valid file-name!")


@error_handler
def import_contacts_from_csv(book: ContactsBook, args: list = ["./data/contacts.csv"]):    
    file_name, *_ = args
    file_name = file_name.lower().strip()
    if not file_name.endswith(".csv"):
        raise WrongFileName
    
    file_name = Path(file_name)

    try:
        with open(file_name, "r", newline="", encoding="UTF-8") as file: 
            reader =  csv.reader(file, delimiter=",")
            next(reader) # Pass the header line
            for line in reader:
                if line not in ["", " ", "-", "—", "\n"]:
                    name, phones, birthday, emails, address, tags \
                        = [value.strip() for value in line]
                    if name not in ["-", "—", ""]:
                        record = Record(name)
                        book.add_record(record) 
                        if phones not in ["-", "—", ""]:
                            for phone in phones.split(";"):
                                record.add_phone(phone)
                        if birthday not in ["-", "—", ""]:
                            record.add_birthday(birthday)
                        if emails not in ["-", "—", ""]:
                            for email in emails.split(";"):
                                record.add_email("email@i.com")
                        if address not in ["-", "—", ""]:
                            record.add_address(address.strip("()"))
                        if tags not in ["-", "—", ""]:
                            for tag in tags.split(";"):
                                record.add_tag(tag)
            
        output_info(f"Import from '{file_name}' successful!")

    except FileNotFoundError:
        output_error(f"File '{file_name}' not found!")
    except OSError:
        output_error(f"Name of '{file_name}' file contains invalid argument! Please, give me a valid file-name!")
    except Exception:
        output_error(f"An ERROR occurred! Check the format for '{file_name}' data.")


@error_handler
def export_notes_to_folder(notes_book: Notes, args: list = ["./data/notes"]):
    folder_name, *_ = args
    if not notes_book:
        output_info(f"Export to '{folder_name}' is impossible. NotesBook is empty yet!")
        return

    folder_name = Path(folder_name)
    folder_name.mkdir(parents=True, exist_ok=True)

    try:
        for id, note in notes_book.items():
            # Remove all unacceptable characters in the note's title
            pattern = r"[;,\-:?\*\|\"\/\\\<\> \+\=]"
            replacement = "_"
            note_title = re.sub(pattern, replacement, note.title._value)
            file_name = f"{folder_name}/{id} - {note_title}.txt"
            
            with open(file_name, "w+", newline="", encoding="UTF-8") as file:
                file.write(f"{note.context._value}\n\n")
                if note.tags:
                    tags = "#" + " | #".join([str(tag) for tag in note.tags])
                    file.write(f"Tags: {tags}\n")
                    file.write(f"     Created at | {note.created_at}\n")
                    file.write(f"Last updated at | {note.updated_at}\n")

    except OSError:
        output_error(f"Name of '{file_name}' file contains invalid argument! Please, give me a valid file-name!")