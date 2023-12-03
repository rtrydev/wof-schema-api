import dataclasses
import json

import inject

from application.config.dependency_injection import di_config
from application.controllers.schema_controller import SchemaController


def handler(event, context):
    if not inject.is_configured():
        inject.configure(di_config)

    schema_controller: SchemaController = inject.instance(SchemaController)

    path_parameters = event.get('pathParameters') or {}
    schema_id = path_parameters.get('id')

    schema = schema_controller.get_schema(schema_id)

    if schema is None:
        return {
            'statusCode': 404
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            'data': dataclasses.asdict(schema)
        })
    }
