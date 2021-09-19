import json

import pytest

from bug_killer.api.bug import create_bug_handler, delete_bug_handler
from bug_killer.domain.response import HttpStatusCodes, message_body
from bug_killer.models.dto.bug import BugResponse
from test.helpers import (
    create_event,
    assert_response,
    assert_dict_attributes_not_none,
    assert_dict_attributes_equals
)
from test.test_doubles.db.projects import (
    populate_project_table_with_project_items,
    api_project_add_bug,
    api_project_delete_bug,
    api_bug_to_delete
)


# This is needed so that the import is not marked as unused
_ = populate_project_table_with_project_items


@pytest.mark.parametrize("evt,expected_status,expected_body", [
    (
            create_event(),
            HttpStatusCodes.UNAUTHORIZED_STATUS,
            message_body('Missing authorization header value')
    ),
    (
            create_event(headers={'cognito:username': 'create_bug_user'}),
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required body parameter "projectId" in request')
    ),
    (
            create_event(
                headers={'cognito:username': 'invalid user'},
                body={
                    'projectId': api_project_add_bug.id,
                    'title': 'test',
                    'description': 'test'
                }
            ),
            HttpStatusCodes.UNAUTHORIZED_STATUS,
            message_body(
                f'"invalid user" does not have permission to make changes to project {api_project_add_bug.id}'
            )
    ),
    (
            create_event(
                headers={'cognito:username': 'create_bug_user'},
                body={
                    'projectId': 'Does not exist',
                    'title': 'test',
                    'description': 'test'
                }
            ),
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body('No project found with id: "Does not exist"')
    )
])
def test_create_bug_handler_invalid_request(
        evt,
        expected_status,
        expected_body,
        populate_project_table_with_project_items
):
    rsp = create_bug_handler(evt, None)
    assert_response(rsp, expected_status, expected_body)


def test_create_bug_handler_valid_request(populate_project_table_with_project_items):
    title = 'test bug title'
    description = 'test bug description'
    tags = ['test']
    payload = {
        'projectId': api_project_add_bug.id,
        'title': title,
        'description': description,
        'tags': tags
    }
    evt = create_event(
        headers={'cognito:username': api_project_add_bug.manager},
        body=payload
    )

    rsp = create_bug_handler(evt, None)

    assert_response(rsp, HttpStatusCodes.CREATED_STATUS)
    assert json.loads(rsp['body'])['projectId'] is not None
    bug = json.loads(rsp['body'])['bug']
    assert_dict_attributes_not_none(bug, ['id', 'createdOn', 'lastUpdatedOn'])
    assert_dict_attributes_equals(bug, {'title': title, 'description': description, 'tags': tags, 'resolved': None})


@pytest.mark.parametrize("evt,expected_status,expected_body", [
    (
            create_event(),
            HttpStatusCodes.UNAUTHORIZED_STATUS,
            message_body('Missing authorization header value')
    ),
    (
            create_event(headers={'cognito:username': 'user'}),
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required body parameter "projectId" in request')
    ),
    (
            create_event(
                headers={'cognito:username': api_project_delete_bug.manager},
                body={
                    'projectId': api_project_delete_bug.id,
                    'bugId': 'Does not exist'
                }
            ),
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body('No bug found with id: "Does not exist"')
    ),
    (
            create_event(
                headers={'cognito:username': api_project_delete_bug.manager},
                body={
                    'projectId': api_project_delete_bug.id,
                    'bugId': api_bug_to_delete.id
                },

            ),
            HttpStatusCodes.OK_STATUS,
            BugResponse(api_project_delete_bug.id, api_bug_to_delete).to_dict()
    )
])
def test_delete_bug_handler(
        evt,
        expected_status,
        expected_body,
        populate_project_table_with_project_items
):
    rsp = delete_bug_handler(evt, None)
    assert_response(rsp, expected_status, expected_body)
