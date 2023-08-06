# coding: utf-8
"""
Script for updating an action in SampleDB.

Usage: python -m sampledb update_action <action_id> <name> <description> <schema_file_name>
"""

import json
import sys
from .. import create_app
from ..logic.actions import update_action, get_action
from ..logic.schemas import validate_schema
from ..logic.errors import ActionDoesNotExistError, ValidationError


def main(arguments):
    if len(arguments) != 4:
        print(__doc__)
        exit(1)
    action_id, name, description, schema_file_name = arguments
    try:
        action_id = int(action_id)
    except ValueError:
        print("Error: action_id must be an integer", file=sys.stderr)
        exit(1)

    app = create_app()
    with app.app_context():
        try:
            action = get_action(action_id)
        except ActionDoesNotExistError:
            print('Error: no action with this id exists', file=sys.stderr)
            exit(1)
        with open(schema_file_name, 'r', encoding='utf-8') as schema_file:
            schema = json.load(schema_file)
        try:
            validate_schema(schema)
        except ValidationError as e:
            print('Error: invalid schema: {}'.format(str(e)), file=sys.stderr)
            exit(1)
        update_action(
            action_id=action.id,
            name=name,
            description=description,
            schema=schema
        )
        print("Success: the action has been updated in SampleDB")
