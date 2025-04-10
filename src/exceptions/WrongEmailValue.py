class WrongEmailValue(Exception):
    """Exception raised for errors in the email value."""

    def __init__(self, message="The provided email value is invalid."):
        self.message = message
        super().__init__(self.message)
