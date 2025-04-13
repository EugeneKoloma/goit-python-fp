from output import output_error


class WrongFileName(Exception):
    def __init__(self, message="Wrong file name."):
        self.message = output_error(message + " Example: file-name.csv")
        super().__init__(self.message)
