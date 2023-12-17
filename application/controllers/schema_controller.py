import uuid
from typing import Optional

import inject

from application.dtos.element.element_read_dto import ElementReadDTO
from application.dtos.schema.schema_read_dto import SchemaReadDTO
from application.dtos.schema.schema_write_dto import SchemaWriteDTO
from domain.models.element import Element
from domain.models.schema import Schema
from domain.repositories.schema_repository import SchemaRepository


class SchemaController:
    @inject.autoparams()
    def __init__(self, schema_repository: SchemaRepository):
        self.schema_repository = schema_repository

    def get_schema(self, schema_id: str) -> Optional[SchemaReadDTO]:
        schema = self.schema_repository.get_by_id(schema_id)

        if schema is None:
            return None

        return SchemaReadDTO(
            id=schema.id,
            name=schema.name,
            elements=list(
                map(lambda element: ElementReadDTO(
                    id=element.id,
                    text=element.text
                ), schema.elements)
            )
        )

    def create_schema(self, schema_data: SchemaWriteDTO) -> Optional[str]:
        schema_id = str(uuid.uuid4())

        schema = Schema(
            id=schema_id,
            name=schema_data.name,
            owner_id=schema_data.owner_id,
            elements=list(map(
                lambda element: Element(
                    id=str(uuid.uuid4()),
                    text=element.text
                ), schema_data.elements
            ))
        )

        if not self.schema_repository.create(schema):
            return None

        return schema_id

    def update_schema(self, schema_id: str, schema_data: SchemaWriteDTO) -> bool:
        existing_schema = self.schema_repository.get_by_id(schema_id)

        if existing_schema is None or existing_schema.owner_id != schema_data.owner_id:
            return False

        schema = Schema(
            id=existing_schema.id,
            name=schema_data.name,
            owner_id=existing_schema.owner_id,
            elements=list(map(
                lambda element: Element(
                    id=str(uuid.uuid4()),
                    text=element.text
                ), schema_data.elements
            ))
        )

        return self.schema_repository.update(schema)
