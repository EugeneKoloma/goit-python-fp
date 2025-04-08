from output import output_error


class WrongPhoneNumber(Exception):
    def __init__(self, message="Wrong number."):
        self.message = output_error(message + " Example: +380112223344")
        super().__init__(self.message)
