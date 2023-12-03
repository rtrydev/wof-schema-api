from abc import ABC, abstractmethod

from domain.models.schema import Schema


class SchemaRepository(ABC):
    @abstractmethod
    def get_by_id(self, schema_id: str) -> Schema:
        pass

    @abstractmethod
    def create(self, schema: Schema) -> bool:
        pass

    @abstractmethod
    def update(self, schema: Schema) -> bool:
        pass
