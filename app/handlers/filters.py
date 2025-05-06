from typing import Callable


def filter_for_command(command: str) -> Callable[[tuple[str]], bool]:
    return lambda callback_data: callback_data[0] == command
