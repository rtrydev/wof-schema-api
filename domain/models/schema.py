from dataclasses import dataclass

from domain.models.element import Element


@dataclass
class Schema:
    id: str
    name: str
    owner_id: str
    elements: list[Element]
