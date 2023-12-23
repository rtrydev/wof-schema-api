from dataclasses import dataclass

from application.dtos.element.element_read_dto import ElementReadDTO
from application.dtos.variable.variable_read_dto import VariableReadDTO


@dataclass
class SchemaReadDTO:
    id: str
    name: str
    elements: list[ElementReadDTO]
    variables: list[VariableReadDTO]
