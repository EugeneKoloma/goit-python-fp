from output import output_error


class PhoneAlreadyOwned(Exception):
    def __init__(self, message="Phone already owned"):
        self.message = output_error(message)
        super().__init__(self.message)
