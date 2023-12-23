from dataclasses import dataclass

from application.dtos.element.element_write_dto import ElementWriteDTO
from application.dtos.variable.variable_write_dto import VariableWriteDTO


@dataclass
class SchemaWriteDTO:
    name: str
    owner_id: str
    elements: list[ElementWriteDTO]
    variables: list[VariableWriteDTO]
