from common import Field


class Title(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self._value = value
        self._max_length = 50

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, title: str):
        if len(title) <= self._max_length:
            self._value = title
        else:
            raise ValueError(
                f"Title length must be less then {self._max_length} characters."
            )


class Context(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self._value = value
        self._max_length = 1000

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, context: str):
        if len(context) <= self._max_length:
            self._value = context
        else:
            raise ValueError(
                f"Context length must less then {self._max_length} characters."
            )
