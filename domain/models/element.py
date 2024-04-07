from dataclasses import dataclass


@dataclass
class Element:
    id: str
    text: str
    locked: bool = False
