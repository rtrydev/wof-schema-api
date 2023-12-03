from domain.repositories.schema_repository import SchemaRepository
from infrastructure.repositories.txt_schema_repository import TXTSchemaRepository


def di_config(binder):
    binder.bind(SchemaRepository, TXTSchemaRepository())
