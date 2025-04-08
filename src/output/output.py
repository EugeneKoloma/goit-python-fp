from colorama import Fore


def output_info(message):
    print(f"{Fore.GREEN}[INFO]: {Fore.RESET}{message}")


def output_error(message):
    print(f"{Fore.RED}[ERROR]: {Fore.RESET}{message}")


def output_warning(message):
    print(f"{Fore.YELLOW}[WARNING]: {Fore.RESET}{message}")


if __name__ == "__main__":
    output_info("This is an info message.")
    output_error("This is an error message.")
    output_warning("This is a warning message.")
