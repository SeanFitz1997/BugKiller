import json
from unittest import TestCase
from unittest.mock import patch

import arrow

from bug_killer_app.access.entities.project import create_project
from bug_killer_app.api.project import get_user_projects_handler, create_project_handler, update_project_handler, \
    delete_project_handler, get_project_handler
from bug_killer_app.domain.response import HttpStatusCodes, message_body
from bug_killer_app.test.helpers import create_event, assert_response, assert_dict_attributes_not_none, \
    assert_dict_attributes_equals, create_cognito_authorizer_request_context
from bug_killer_app.test.test_doubles.db.transact_write import DummyTransactWrite
from bug_killer_schemas.request.project import UpdateProjectPayload
from bug_killer_schemas.response.project import UserProjectsResponse, ProjectResponse
from bug_killer_schemas.test.doubles.request.project import create_test_create_project_payload
from bug_killer_utils.collections import remove_none_values_from_dict
from bug_killer_utils.function import run_async


class TestGetUserProjects(TestCase):
    TEST_NAME = 'GetUserProjects'
    USER_WITH_PROJECTS = f'{TEST_NAME}_USER_WITH_PROJECTS'
    USER_WITHOUT_PROJECTS = f'{TEST_NAME}_USER_WITHOUT_PROJECTS'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        manager_project_future = create_project(
            TestGetUserProjects.USER_WITH_PROJECTS,
            create_test_create_project_payload()
        )
        member_project_future = create_project(
            'some_other_user',
            create_test_create_project_payload(members=[cls.USER_WITH_PROJECTS])
        )

        cls.manager_project = run_async(manager_project_future)
        cls.member_project = run_async(member_project_future)

    def test_error_when_missing_auth_header(self):
        # Given
        evt = create_event()

        # When
        rsp = get_user_projects_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_user_with_no_projects(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context(self.USER_WITHOUT_PROJECTS))

        # When
        rsp = get_user_projects_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.OK_STATUS, UserProjectsResponse().api_dict())

    def test_user_with_projects(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context(self.USER_WITH_PROJECTS))

        # When
        rsp = get_user_projects_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.OK_STATUS,
            UserProjectsResponse(
                manager_projects=[self.manager_project],
                member_projects=[self.member_project]
            ).api_dict()
        )


class TestGetProject(TestCase):
    TEST_NAME = 'GetProject'
    USER1 = f'{TEST_NAME}_USER_1'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        get_project_future = create_project(cls.USER1, create_test_create_project_payload())

        cls.get_project = run_async(get_project_future)

    def test_error_when_missing_auth_header(self):
        # Given
        event_without_auth_header = create_event()

        # When
        rsp = get_project_handler(event_without_auth_header, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_missing_id_path_param(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context('user'))

        # When
        rsp = get_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required pathParameters parameter "projectId" in request')
        )

    def test_error_when_project_not_found(self):
        # Given
        project_id = 'does_not_exist'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context('user'),
            path={'projectId': project_id}
        )

        # When
        rsp = get_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body(f'No project found with id: "{project_id}"')
        )

    def test_error_when_user_cant_access_project(self):
        # Given
        user = 'invalid_user'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(user),
            path={'projectId': self.get_project.id}
        )

        # When
        rsp = get_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.FORBIDDEN_STATUS,
            message_body(f'{user} does not have permission to read project {self.get_project.id}')
        )

    def test_user_get_project(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'projectId': self.get_project.id}
        )

        # When
        rsp = get_project_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.OK_STATUS, ProjectResponse(project=self.get_project).api_dict())


class TestCreateProject(TestCase):

    def test_error_when_missing_auth_header(self):
        # Given
        event_without_auth_header = create_event()

        # When
        rsp = create_project_handler(event_without_auth_header, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_missing_required_param(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context('user'))

        # When
        rsp = create_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required body parameter "title" in request')
        )

    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def test_user_creates_project(self):
        # Given
        user = 'user'
        payload = create_test_create_project_payload()
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(user),
            body=payload.api_dict()
        )

        # When
        rsp = create_project_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.CREATED_STATUS)
        project = json.loads(rsp['body'])['project']
        assert_dict_attributes_not_none(project, ['id', 'createdOn', 'lastUpdatedOn'])
        assert_dict_attributes_equals(project, {**payload.api_dict(), 'manager': user, 'bugs': []})


class TestUpdateProject(TestCase):
    TEST_NAME = 'UpdateProject'
    USER1 = f'{TEST_NAME}_USER_1'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        update_project_future = create_project(cls.USER1, create_test_create_project_payload())

        cls.update_project = run_async(update_project_future)

    def test_error_when_missing_auth_header(self):
        # Given
        event_without_auth_header = create_event()

        # When
        rsp = update_project_handler(event_without_auth_header, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_user_lacks_permission_to_update(self):
        # Given
        user = 'invalid_user'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(user),
            path={'projectId': self.update_project.id},
            body=UpdateProjectPayload(manager='new_manager').api_dict()
        )

        # When
        rsp = update_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.FORBIDDEN_STATUS,
            message_body(f'{user} does not have permission to update project {self.update_project.id}')
        )

    def test_error_when_project_not_found(self):
        # Given
        project_id = 'does_not_exist'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context('invalid user'),
            path={'projectId': project_id},
            body=UpdateProjectPayload(manager='new_manager').api_dict()
        )

        # When
        rsp = update_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body(f'No project found with id: "{project_id}"')
        )

    def test_error_when_empty_update(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'projectId': self.update_project.id},
            body=UpdateProjectPayload().api_dict()
        )

        # When
        rsp = update_project_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.BAD_REQUEST_STATUS, message_body('No changes provided in update payload'))

    def test_error_changes_match_the_existing_item(self):
        # Given
        payload = UpdateProjectPayload(
            title=self.update_project.title,
            description=self.update_project.description
        )
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'projectId': self.update_project.id},
            body=payload.api_dict()
        )

        # When
        rsp = update_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('All changes in payload matches the existing record')
        )

    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def test_project_update(self):
        # Given
        payload = UpdateProjectPayload(
            manager='updated manager',
            title='updated title',
            description='updated description'
        )
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.update_project.manager),
            path={'projectId': self.update_project.id},
            body=payload.api_dict()
        )

        # When
        rsp = update_project_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.OK_STATUS)
        project = json.loads(rsp['body'])['project']

        assert_dict_attributes_not_none(project, ['id', 'createdOn'])
        assert_dict_attributes_equals(project, remove_none_values_from_dict(payload.api_dict()))
        assert arrow.get(project['lastUpdatedOn']) >= self.update_project.last_updated_on.floor('second')


class TestDeleteProject(TestCase):
    TEST_NAME = 'DeleteProject'
    USER1 = f'{TEST_NAME}_USER_1'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        delete_project_future = create_project(cls.USER1, create_test_create_project_payload())
        lack_access_project_future = create_project(cls.USER1, create_test_create_project_payload())

        cls.delete_project = run_async(delete_project_future)
        cls.lack_access_project = run_async(lack_access_project_future)

    def test_error_when_missing_auth_header(self):
        # Given
        evt = create_event()

        # When
        rsp = delete_project_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_user_lacks_permission(self):
        # Given
        user = 'invalid_user'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(user),
            path={'projectId': self.lack_access_project.id}
        )

        # When
        rsp = delete_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.FORBIDDEN_STATUS,
            message_body(f'{user} does not have permission to update project {self.lack_access_project.id}')
        )

    def test_error_when_project_not_found(self):
        # Given
        project_id = 'does_not_exist'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context('manager'),
            path={'projectId': project_id}
        )

        # When
        rsp = delete_project_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body(f'No project found with id: "{project_id}"')
        )

    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def test_delete_project(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'projectId': self.delete_project.id}
        )

        # When
        rsp = delete_project_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.OK_STATUS, ProjectResponse(project=self.delete_project).api_dict())
