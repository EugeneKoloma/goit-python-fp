from output import output_error


class EmailAlreadyOwned(Exception):
    def __init__(self, message="Email already owned"):
        self.message = output_error(message)
        super().__init__(self.message)
