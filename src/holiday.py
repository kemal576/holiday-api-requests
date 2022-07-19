from dataclasses import dataclass
from datetime import datetime


@dataclass
class Holiday:
    name: str
    date: datetime
    public: bool
    country: str
    weekday: dict
    observed: dict
    uuid: str

    def __str__(self):
        weekday = self.weekday['date']['name']
        is_public = "Public" if self.public else "Not Public"
        return f"{self.name} / {self.date} {weekday} / {is_public}"
