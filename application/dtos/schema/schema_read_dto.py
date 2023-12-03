from dataclasses import dataclass

from application.dtos.element.element_read_dto import ElementReadDTO


@dataclass
class SchemaReadDTO:
    id: str
    elements: list[ElementReadDTO]
