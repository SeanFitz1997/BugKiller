import json

import arrow
import pytest

from bug_killer.api.project import (
    get_user_projects_handler,
    create_project_handler,
    update_project_handler,
    delete_project_handler
)
from bug_killer.domain.response import HttpStatusCodes, message_body
from bug_killer.models.dto.project import UserProjectsResponse, ProjectResponse
from bug_killer.util.dates import to_utc_str
from test.helpers import (
    create_event,
    assert_response,
    assert_dict_attributes_not_none,
    assert_dict_attributes_equals
)
from test.test_doubles.db.projects import (
    populate_project_table_with_project_items,
    user_with_projects,
    user_without_projects,
    manager_project,
    member_projects,
    api_project_to_update,
    api_project_to_delete,
    api_project_no_op_update
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
            create_event(headers={'cognito:username': user_without_projects}),
            HttpStatusCodes.OK_STATUS,
            UserProjectsResponse().to_dict()
    ),
    (
            create_event(headers={'cognito:username': user_with_projects}),
            HttpStatusCodes.OK_STATUS,
            UserProjectsResponse(
                manger_projects=[manager_project],
                member_projects=member_projects
            ).to_dict()
    )
])
def test_get_user_projects_handler(
        evt,
        expected_status,
        expected_body,
        populate_project_table_with_project_items
):
    rsp = get_user_projects_handler(evt, None)
    assert_response(rsp, expected_status, expected_body)


@pytest.mark.parametrize("evt,expected_status,expected_body", [
    (
            create_event(),
            HttpStatusCodes.UNAUTHORIZED_STATUS,
            message_body('Missing authorization header value')
    ),
    (
            create_event(headers={'cognito:username': 'create_projects_user'}),
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body("Missing required body parameter 'title' in request")
    )
])
def test_create_project_handler_invalid_request(evt, expected_status, expected_body):
    rsp = create_project_handler(evt, None)
    assert_response(rsp, expected_status, expected_body)


def test_create_project_handler_valid_request():
    payload = {
        'title': 'test',
        'description': '123',
        'tags': ['test'],
        'members': ['123']
    }
    user = 'create_user'
    evt = create_event(
        headers={'cognito:username': user},
        body=payload
    )
    rsp = create_project_handler(evt, None)

    assert_response(rsp, HttpStatusCodes.CREATED_STATUS)
    project = json.loads(rsp['body'])['project']
    assert_dict_attributes_not_none(project, ['id', 'createdOn', 'lastUpdatedOn'])
    assert_dict_attributes_equals(project, {**payload, 'manager': user, 'bugs': []})


@pytest.mark.parametrize("evt,expected_status,expected_body", [
    (
            create_event(),
            HttpStatusCodes.UNAUTHORIZED_STATUS,
            message_body('Missing authorization header value')
    ),
    (
            create_event(
                headers={'cognito:username': 'invalid user'},
                path={'projectId': api_project_to_update.id},
                body={'manager': 'new manager'}
            ),
            HttpStatusCodes.UNAUTHORIZED_STATUS,
            message_body(
                f'"invalid user" does not have permission to make changes to project {api_project_to_update.id}'
            )
    ),
    (
            create_event(
                headers={'cognito:username': 'invalid user'},
                path={'projectId': 'does not exist'},
                body={'manager': 'manager'}
            ),
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body(f'No project found with id: "does not exist"')
    )
])
def test_update_project_handler_invalid_request(evt, expected_status, expected_body):
    rsp = update_project_handler(evt, None)
    assert_response(rsp, expected_status, expected_body)


def test_update_project_handler_valid_request():
    update_payload = {
        'manager': 'updated manager',
        'title': 'updated title',
        'description': 'updated description'
    }
    evt = create_event(
        headers={'cognito:username': api_project_to_update.manager},
        path={'projectId': api_project_to_update.id},
        body=update_payload
    )
    rsp = update_project_handler(evt, None)

    assert_response(rsp, HttpStatusCodes.OK_STATUS)
    project = json.loads(rsp['body'])['project']
    assert_dict_attributes_not_none(project, ['id', 'createdOn'])
    assert_dict_attributes_equals(project, update_payload)
    assert arrow.get(project['lastUpdatedOn']) > api_project_to_update.last_updated_on


def test_update_project_handler_no_op_request():
    evt = create_event(
        headers={'cognito:username': api_project_no_op_update.manager},
        path={'projectId': api_project_no_op_update.id},
        body={}
    )
    rsp = update_project_handler(evt, None)

    assert_response(rsp, HttpStatusCodes.OK_STATUS)
    project = json.loads(rsp['body'])['project']
    assert_dict_attributes_not_none(project, ['id', 'createdOn'])
    assert project['lastUpdatedOn'] == to_utc_str(api_project_no_op_update.last_updated_on)


@pytest.mark.parametrize("evt,expected_status,expected_body", [
    (
            create_event(),
            HttpStatusCodes.UNAUTHORIZED_STATUS,
            message_body('Missing authorization header value')
    ),
    (
            create_event(
                headers={'cognito:username': 'invalid user'},
                path={'projectId': api_project_to_delete.id}
            ),
            HttpStatusCodes.UNAUTHORIZED_STATUS,
            message_body(
                f'"invalid user" does not have permission to make changes to project {api_project_to_delete.id}'
            )
    ),
    (
            create_event(
                headers={'cognito:username': 'manager'},
                path={'projectId': 'this does not exist'}
            ),
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body('No project found with id: "this does not exist"')
    ),
    (
            create_event(
                headers={'cognito:username': api_project_to_delete.manager},
                path={'projectId': api_project_to_delete.id}
            ),
            HttpStatusCodes.OK_STATUS,
            ProjectResponse(api_project_to_delete).to_dict()
    )
])
def test_delete_project_handler(evt, expected_status, expected_body):
    rsp = delete_project_handler(evt, None)
    assert_response(rsp, expected_status, expected_body)
