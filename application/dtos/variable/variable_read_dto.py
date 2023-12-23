from dataclasses import dataclass


@dataclass
class VariableReadDTO:
    variable_name: str
    wheel_id: str
