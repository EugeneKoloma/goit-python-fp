from output import output_error


class InvalidDaysInput(Exception):
    def __init__(
        self, message="Invalid number of days. Please provide a valid integer."
    ):
        self.message = output_error(message)
        super().__init__(self.message)
