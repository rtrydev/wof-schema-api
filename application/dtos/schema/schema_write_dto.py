from dataclasses import dataclass

from application.dtos.element.element_write_dto import ElementWriteDTO


@dataclass
class SchemaWriteDTO:
    elements: list[ElementWriteDTO]
