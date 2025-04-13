import csv

from output import default_contacts_table_fields
from decorators import error_handler
from exceptions import WrongFileName
from output import output_error, output_info

from contacts.ContactsBook import ContactsBook
from contacts.Records import Record


@error_handler
def export_contacts_to_csv(book: ContactsBook, args: list = [".\\data\\contacts.csv"]):
    file_name, *fields = args
    file_name = file_name.lower().strip()
    if not file_name.endswith(".csv"):
        raise WrongFileName

    if not fields:
        fields = default_contacts_table_fields
    else:
        fields = [
            field
            for field in default_contacts_table_fields
            if field.lower() in fields
        ]
        if "Name" not in fields:
            fields.insert(0, "Name")

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

                whole_data = {
                    "Name": name,
                    "Phones": phones,
                    "Birthday": birthday,
                    "Emails": emails,
                    "Address": address,
                    "Tags": tags,
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
def import_contacts_to_csv(book: ContactsBook, args: list = [".\\data\\contacts.csv"]):    
    file_name, *_ = args
    file_name = file_name.lower().strip()
    if not file_name.endswith(".csv"):
        raise WrongFileName

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