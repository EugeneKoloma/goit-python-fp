from output import output_error


class RecordNotFound(Exception):
    def __init__(self, message="Record not found"):
        self.message = output_error(message)
        super().__init__(self.message)
