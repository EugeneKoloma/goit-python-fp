from output import output_error


class WrongDateFormat(Exception):
    def __init__(self, message="Wrong date format."):
        self.message = output_error(message + " Example: 01.01.2025 ~ DD.MM.YYYY")
        super().__init__(self.message)
