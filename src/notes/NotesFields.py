from datetime import datetime

from common import Field


class Title(Field):
    pass
    

class NoteString(Field):
    pass


class GetTime(Field):
    
    @property
    def time(self) -> str:
        if type(self._value) == datetime:
            return self._value.strftime("%d %B %Y at %H:%M:%S")
    
    @time.setter
    def time(self, date):
        self._value = date