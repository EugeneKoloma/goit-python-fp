"""
Elastic Search Utility
=======================

Purpose:
--------
This module provides a lightweight elastic search function for filtering contact or note records
by a query string. It searches across all string-representable fields of each record.

Use Cases:
----------
- Search contacts by name, phone, email, or tags.
- Search notes by title, content, or tags (future use).

The search is case-insensitive and tolerant to different data shapes.

Usage Example:
--------------
    from utils.search import elastic_search
    results = elastic_search(contact_book.data.values(), "urgent")
    for record in results:
        print(record)

Note:
-----
`record.get_all_fields()` should return a list of string-convertible fields like name, phone, email, tags, etc.
This method needs to be implemented on the Record class or adapted per model.
"""

def elastic_search(records, query: str):
    filtered = []
    query = query.lower()
    for record in records:
        try:
            searchable = " ".join([
                str(field).lower()
                for field in record.get_all_fields()
                if isinstance(field, str) or hasattr(field, '__str__')
            ])
            if query in searchable:
                filtered.append(record)
        except Exception:
            continue
    return filtered
