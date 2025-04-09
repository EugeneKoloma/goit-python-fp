from output import output_error


class WrongEmail(Exception):
    def __init__(self, message="Wrong email format."):
        self.message = output_error(message + " Example: example@mail.com")
        super().__init__(self.message)
