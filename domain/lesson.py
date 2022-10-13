from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Lesson:
    name: str
    start: str
    end: str
    info: str
    url: str
    additional_info: Optional[str]
