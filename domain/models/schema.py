from dataclasses import dataclass

from domain.models.element import Element
from domain.models.variable import Variable


@dataclass
class Schema:
    id: str
    name: str
    owner_id: str
    variables: list[Variable]
    elements: list[Element]
