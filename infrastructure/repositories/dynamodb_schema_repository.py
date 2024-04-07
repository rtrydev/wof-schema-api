import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from domain.models.element import Element
from domain.models.schema import Schema
from domain.models.variable import Variable
from domain.repositories.schema_repository import SchemaRepository


class DynamoDBSchemaRepository(SchemaRepository):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('wof-schemas')

    def get_for_user(self, user_id: str) -> list[Schema]:
        try:
            response = self.table.query(
                IndexName='owner_id-index',
                KeyConditionExpression=Key('owner_id').eq(user_id)
            )

            items = response.get('Items', [])

            return [
                Schema(
                    id=item['id'],
                    name=item['name'],
                    owner_id=item['owner_id'],
                    elements=[Element(**element) for element in item.get('elements', [])],
                    variables=[Variable(**variable) for variable in item.get('variables', [])]
                )
                for item in items
            ]
        except ClientError as e:
            print(f"Error fetching schema: {e}")
        return []

    def get_by_id(self, schema_id: str) -> Schema:
        try:
            response = self.table.get_item(Key={'id': schema_id})
            if 'Item' in response:
                item = response['Item']
                return Schema(
                    id=item['id'],
                    name=item['name'],
                    owner_id=item['owner_id'],
                    elements=[Element(**element) for element in item.get('elements', [])],
                    variables=[Variable(**variable) for variable in item.get('variables', [])]
                )
        except ClientError as e:
            print(f"Error fetching schema: {e}")
        return None

    def create(self, schema: Schema) -> bool:
        try:
            elements = [{'id': e.id, 'text': e.text} for e in schema.elements]
            variables = [{'variable_name': v.variable_name, 'wheel_id': v.wheel_id} for v in schema.variables]

            self.table.put_item(Item={
                'id': schema.id,
                'name': schema.name,
                'owner_id': schema.owner_id,
                'elements': elements,
                'variables': variables
            })
            return True
        except ClientError as e:
            print(f"Error creating schema: {e}")
            return False

    def update(self, schema: Schema) -> bool:
        try:
            elements = [{'id': e.id, 'text': e.text, 'locked': e.locked} for e in schema.elements]
            variables = [{'variable_name': v.variable_name, 'wheel_id': v.wheel_id} for v in schema.variables]

            self.table.update_item(
                Key={'id': schema.id},
                UpdateExpression="set #wheel_name = :n, elements = :e, variables = :v",
                ExpressionAttributeNames={
                    '#wheel_name': 'name'
                },
                ExpressionAttributeValues={
                    ':n': schema.name,
                    ':e': elements,
                    ':v': variables
                }
            )

            return True
        except ClientError as e:
            print(f"Error updating schema: {e}")
            return False
