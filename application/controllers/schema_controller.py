import uuid
from typing import Optional
import dataclasses

import inject
from deepdiff import DeepDiff

from application.dtos.element.element_read_dto import ElementReadDTO
from application.dtos.schema.schema_read_dto import SchemaReadDTO
from application.dtos.schema.schema_write_dto import SchemaWriteDTO
from application.dtos.variable.variable_read_dto import VariableReadDTO
from domain.models.element import Element
from domain.models.schema import Schema
from domain.models.variable import Variable
from domain.repositories.collaboration_repository import CollaborationAffiliationRepository
from domain.repositories.schema_repository import SchemaRepository


class SchemaController:
    @inject.autoparams()
    def __init__(self, schema_repository: SchemaRepository, affiliation_repository: CollaborationAffiliationRepository):
        self.schema_repository = schema_repository
        self.affiliation_repository = affiliation_repository

    def get_schemas(self, user_id: str) -> list[SchemaReadDTO]:
        schemas = self.schema_repository.get_for_user(user_id)

        return [
            SchemaReadDTO(
                id=schema.id,
                name=schema.name,
                elements=list(
                    map(lambda element: ElementReadDTO(
                        id=element.id,
                        text=element.text,
                        locked=element.locked
                    ), schema.elements)
                ),
                variables=list(
                    map(lambda variable: VariableReadDTO(
                        variable_name=variable.variable_name,
                        wheel_id=variable.wheel_id
                    ), schema.variables)
                )
            )
            for schema in schemas
        ]

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
                    text=element.text,
                    locked=element.locked
                ), schema.elements)
            ),
            variables=list(
                map(lambda variable: VariableReadDTO(
                    variable_name=variable.variable_name,
                    wheel_id=variable.wheel_id
                ), schema.variables)
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
                    text=element.text,
                    locked=element.locked
                ), schema_data.elements
            )),
            variables=list(
                map(lambda variable: Variable(
                    variable_name=variable.variable_name,
                    wheel_id=variable.wheel_id
                ), schema_data.variables)
            )
        )

        if not self.schema_repository.create(schema):
            return None

        return schema_id

    def update_schema(self, schema_id: str, schema_data: SchemaWriteDTO) -> bool:
        existing_schema = self.schema_repository.get_by_id(schema_id)

        if existing_schema is None:
            return False

        if existing_schema.owner_id != schema_data.owner_id:
            user_affiliations = self.affiliation_repository.get_by_user_id(schema_data.owner_id)

            if not any([
                schema_id == affiliation.schema_id
                for affiliation in user_affiliations
            ]):
                return False

        schema = Schema(
            id=existing_schema.id,
            name=schema_data.name,
            owner_id=existing_schema.owner_id,
            elements=list(map(
                lambda element: Element(
                    id=str(uuid.uuid4()),
                    text=element.text,
                    locked=element.locked
                ), schema_data.elements
            )),
            variables=list(
                map(lambda variable: Variable(
                    variable_name=variable.variable_name,
                    wheel_id=variable.wheel_id
                ), schema_data.variables)
            )
        )

        diff = DeepDiff(
            dataclasses.asdict(existing_schema),
            dataclasses.asdict(schema),
            exclude_regex_paths=r"root.*\['id'\]"
        )
        change_log = [
            f'Change on path {key}: {value.get("old_value")} -> {value.get("new_value")}'
            for key, value in diff.get('values_changed', {}).items()
        ]
        add_log = [
            f'Added on path {key}: {element}'
            for key, element in diff.get('iterable_item_added', {}).items()
        ]
        remove_log = [
            f'Deleted on path {key}: {element}'
            for key, element in diff.get('iterable_item_removed', {}).items()
        ]

        for log in change_log + add_log + remove_log:
            print(log)

        return self.schema_repository.update(schema)
