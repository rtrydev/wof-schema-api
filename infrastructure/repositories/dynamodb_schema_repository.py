import boto3
from botocore.exceptions import ClientError

from domain.models.element import Element
from domain.models.schema import Schema
from domain.repositories.schema_repository import SchemaRepository


class DynamoDBSchemaRepository(SchemaRepository):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('wof-schemas')

    def get_by_id(self, schema_id: str) -> Schema:
        try:
            response = self.table.get_item(Key={'id': schema_id})
            if 'Item' in response:
                item = response['Item']
                return Schema(
                    id=item['id'],
                    name=item['name'],
                    owner_id=item['owner_id'],
                    elements=[Element(**element) for element in item.get('elements', [])]
                )
        except ClientError as e:
            print(f"Error fetching schema: {e}")
        return None

    def create(self, schema: Schema) -> bool:
        try:
            elements = [{'id': e.id, 'text': e.text} for e in schema.elements]
            self.table.put_item(Item={
                'id': schema.id,
                'name': schema.name,
                'owner_id': schema.owner_id,
                'elements': elements
            })
            return True
        except ClientError as e:
            print(f"Error creating schema: {e}")
            return False

    def update(self, schema: Schema) -> bool:
        try:
            elements = [{'id': e.id, 'text': e.text} for e in schema.elements]
            self.table.update_item(
                Key={'id': schema.id},
                UpdateExpression="set #wheel_name = :n, elements=:e",
                ExpressionAttributeNames={
                    '#wheel_name': 'name'
                },
                ExpressionAttributeValues={
                    ':n': schema.name,
                    ':e': elements
                }
            )
            return True
        except ClientError as e:
            print(f"Error updating schema: {e}")
            return False
