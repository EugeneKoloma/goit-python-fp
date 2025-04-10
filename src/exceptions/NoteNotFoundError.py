from output import output_error


class NoteNotFoundError(Exception):
    def __init__(self, message="There is no any coincidences by your quary!"):
        self.message = output_error(message)
        super().__init__(self.message)
