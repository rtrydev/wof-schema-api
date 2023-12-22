import dataclasses
import json
import inject

from application.config.dependency_injection import di_config
from application.controllers.schema_controller import SchemaController


def handler(event, context):
    user_id = event\
        .get('requestContext', {})\
        .get('authorizer', {})\
        .get('lambda', {})\
        .get('user_id')

    if user_id is None:
        return {
            'statusCode': 401
        }

    if not inject.is_configured():
        inject.configure(di_config)

    schema_controller: SchemaController = inject.instance(SchemaController)
    schemas = schema_controller.get_schemas(user_id)

    return {
        'statusCode': 200,
        'body': json.dumps(
            [dataclasses.asdict(schema) for schema in schemas]
        )
    }

