import dataclasses
import json
from typing import Optional

from domain.models.element import Element
from domain.models.schema import Schema
from domain.repositories.schema_repository import SchemaRepository


class TXTSchemaRepository(SchemaRepository):
    FILE_NAME = 'schema_data.txt'

    def get_by_id(self, schema_id: str) -> Optional[Schema]:
        schema = self.__load_data().get(schema_id)

        if schema is None:
            return None

        return Schema(
            id=schema.get('id'),
            elements=list(map(
                lambda element: Element(
                    id=element.get('id'),
                    text=element.get('text')
                ), schema.get('elements')
            ))
        )

    def create(self, schema: Schema) -> bool:
        data = self.__load_data()

        if data.get(schema.id):
            return False

        data[schema.id] = dataclasses.asdict(schema)
        return self.__save_data(data)

    def update(self, schema: Schema) -> bool:
        data = self.__load_data()
        existing_schema = data.get(schema.id)

        if existing_schema is None:
            return False

        data[schema.id] = dataclasses.asdict(schema)
        return self.__save_data(data)

    def __load_data(self) -> dict:
        try:
            with open(self.FILE_NAME, 'r') as file:
                data = json.loads(file.read())
        except Exception as e:
            print('Could not read data from txt file:', e)
            return {}

        return data

    def __save_data(self, data: dict) -> bool:
        data_string = json.dumps(data)

        try:
            with open(self.FILE_NAME, 'wb') as file:
                file.write(data_string.encode('utf8'))

            return True
        except Exception as e:
            print('Could not save data to txt file:', e)
            return False
