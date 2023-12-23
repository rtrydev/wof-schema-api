from dataclasses import dataclass


@dataclass
class VariableWriteDTO:
    variable_name: str
    wheel_id: str
