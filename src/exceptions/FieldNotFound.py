from output import output_error


class FieldNotFound(Exception):
    def __init__(self, message="Phone not found"):
        self.message = output_error("Phone not found: " + message)
        super().__init__(self.message)
