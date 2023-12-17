from domain.repositories.schema_repository import SchemaRepository
from infrastructure.repositories.dynamodb_schema_repository import DynamoDBSchemaRepository


def di_config(binder):
    binder.bind(SchemaRepository, DynamoDBSchemaRepository())
