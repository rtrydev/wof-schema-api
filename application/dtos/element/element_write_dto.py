from dataclasses import dataclass


@dataclass
class ElementWriteDTO:
    text: str
    locked: bool
