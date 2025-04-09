"""
Exception class for raising exception if tag is not fount in the record
"""

class TagNotFound(Exception):
    """Raised when a tag is not found in a contact record."""
    def __init__(self, tag_value: str):
        super().__init__(f"Tag '{tag_value}' not found in this contact.")
