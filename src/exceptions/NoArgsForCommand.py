from output import output_error


class NoArgsForCommand(Exception):
    def __init__(self, command: str, message="Arguments are empty"):
        self.command = command
        self.message = output_error(
            f"Please, add arguments to your command: {self.command}"
        )
        super().__init__(message)
