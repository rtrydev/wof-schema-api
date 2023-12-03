import json

import inject

from application.config.dependency_injection import di_config
from application.controllers.schema_controller import SchemaController
from application.dtos.element.element_write_dto import ElementWriteDTO
from application.dtos.schema.schema_write_dto import SchemaWriteDTO


def handler(event, context):
    if not inject.is_configured():
        inject.configure(di_config)

    schema_controller: SchemaController = inject.instance(SchemaController)

    path_parameters = event.get('pathParameters') or {}
    schema_id = path_parameters.get('id')

    event_body = json.loads(event.get('body') or '{}')

    schema = SchemaWriteDTO(
        elements=list(map(
            lambda element: ElementWriteDTO(
                text=element.get('text')
            ), event_body.get('elements') or []
        ))
    )

    result = schema_controller.update_schema(schema_id, schema)

    if not result:
        return {
            'statusCode': 404
        }

    return {
        'statusCode': 204
    }