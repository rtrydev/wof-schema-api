import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from typing import List
from domain.models.collaboration_affiliation import CollaborationAffiliation
from domain.repositories.collaboration_repository import CollaborationAffiliationRepository


class DynamoDBCollaborationAffiliationRepository(CollaborationAffiliationRepository):
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('wof-collaboration-affiliations')

    def get_by_user_id(self, user_id: str) -> List[CollaborationAffiliation]:
        try:
            response = self.table.query(
                IndexName='user_id-index',
                KeyConditionExpression=Key('user_id').eq(user_id)
            )

            items = response.get('Items', [])

            if len(items) == 0:
                return []

            return list(
                map(
                    lambda item: CollaborationAffiliation(
                        schema_id=item['schema_id'],
                        user_id=item['user_id']
                    ),
                    items
                )
            )
        except ClientError as e:
            print(f'Error fetching affiliation: {e}')
        return []
