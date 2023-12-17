import json

import inject

from application.config.dependency_injection import di_config
from application.controllers.schema_controller import SchemaController
from application.dtos.element.element_write_dto import ElementWriteDTO
from application.dtos.schema.schema_write_dto import SchemaWriteDTO


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

    event_body = json.loads(event.get('body') or '{}')

    schema = SchemaWriteDTO(
        name=event_body.get('name'),
        owner_id=user_id,
        elements=list(map(
            lambda element: ElementWriteDTO(
                text=element.get('text')
            ), event_body.get('elements') or []
        ))
    )

    result = schema_controller.create_schema(schema)

    if not result:
        return {
            'statusCode': 403
        }

    return {
        'statusCode': 201,
        'body': json.dumps({
            'id': result
        })
    }
