import json
from unittest import TestCase
from unittest.mock import patch

from bug_killer_app.access.entities.bug import create_project_bug, resolve_project_bug
from bug_killer_app.access.entities.project import create_project
from bug_killer_app.api.bug import get_bug_handler, create_bug_handler, update_bug_handler, resolve_bug_handler, \
    delete_bug_handler
from bug_killer_app.domain.response import HttpStatusCodes, message_body
from bug_killer_app.test.helpers import create_event, assert_response, assert_dict_attributes_not_none, \
    assert_dict_attributes_equals, create_cognito_authorizer_request_context
from bug_killer_app.test.test_doubles.db.transact_write import DummyTransactWrite
from bug_killer_schemas.entities.bug import BugResolution
from bug_killer_schemas.request.bug import UpdateBugPayload
from bug_killer_schemas.response.bug import BugResponse
from bug_killer_schemas.test.doubles.request.bug import create_test_create_bug_payload
from bug_killer_schemas.test.doubles.request.project import create_test_create_project_payload
from bug_killer_utils.dates import to_utc_str
from bug_killer_utils.function import run_async


class TestGetBug(TestCase):
    TEST_NAME = 'GetBug'
    USER1 = f'{TEST_NAME}_USER1'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        project_with_bug_future = create_project(
            TestGetBug.USER1,
            create_test_create_project_payload()
        )
        cls.project_with_bug = run_async(project_with_bug_future)

        bug_to_get_future = create_project_bug(
            TestGetBug.USER1,
            create_test_create_bug_payload(cls.project_with_bug.id)
        )
        cls.bug_to_get = run_async(bug_to_get_future)

    def test_error_when_missing_auth_header(self):
        # Given
        evt = create_event()

        # When
        rsp = get_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_missing_id(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context('user'))

        # When
        rsp = get_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required pathParameters parameter "bugId" in request')
        )

    def test_error_when_bug_doesnt_exist(self):
        # Given
        bug_id = 'does_not_exist'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context('user'),
            path={'bugId': bug_id}
        )

        # When
        rsp = get_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.NOT_FOUND_STATUS, message_body(f'No bug found with id: "{bug_id}"'))

    def test_error_when_user_lacks_permission(self):
        # Given
        user = 'lacks_access_user'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(user),
            path={'bugId': self.bug_to_get.id}
        )

        # When
        rsp = get_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.FORBIDDEN_STATUS,
            message_body(f'{user} does not have permission to read project {self.project_with_bug.id}')
        )

    def test_gets_bug(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'bugId': self.bug_to_get.id}
        )

        # When
        rsp = get_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.OK_STATUS,
            BugResponse(project_id=self.project_with_bug.id, bug=self.bug_to_get).api_dict()
        )


class TestCreateBug(TestCase):
    TEST_NAME = 'CreateBug'
    USER1 = f'{TEST_NAME}_USER1'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        project_future = create_project(
            TestCreateBug.USER1,
            create_test_create_project_payload()
        )
        cls.project = run_async(project_future)

    def test_error_when_missing_auth_header(self):
        # Given
        evt = create_event()

        # When
        rsp = create_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_missing_project_id(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context('user'))

        # When
        rsp = create_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required body parameter "projectId" in request')
        )

    def test_error_when_user_lacks_access(self):
        # Given
        user = 'lacks_access'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(user),
            body=create_test_create_bug_payload(self.project.id).api_dict()
        )

        # When
        rsp = create_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.FORBIDDEN_STATUS,
            message_body(f'{user} does not have permission to update project {self.project.id}')
        )

    def test_error_when_project_not_found(self):
        # Given
        project_id = 'does_not_exist'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context('user'),
            body=create_test_create_bug_payload(project_id).api_dict()
        )

        # When
        rsp = create_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body(f'No project found with id: "{project_id}"')
        )

    def test_user_creates_bug(self):
        # Given
        payload = create_test_create_bug_payload(self.project.id)
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            body=payload.api_dict()
        )

        # When
        rsp = create_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.CREATED_STATUS)
        assert json.loads(rsp['body'])['projectId'] is not None
        bug = json.loads(rsp['body'])['bug']
        assert_dict_attributes_not_none(bug, ['id', 'createdOn', 'lastUpdatedOn'])
        assert_dict_attributes_equals(
            bug,
            {'title': payload.title, 'description': payload.description, 'tags': payload.tags, 'resolved': None}
        )


class TestUpdateBug(TestCase):
    TEST_NAME = 'UpdateBug'
    USER1 = f'{TEST_NAME}_USER1'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        project_future = create_project(
            TestUpdateBug.USER1,
            create_test_create_project_payload()
        )
        cls.project = run_async(project_future)

        bug_to_update_future = create_project_bug(cls.USER1, create_test_create_bug_payload(cls.project.id))
        change_update_bug_future = create_project_bug(cls.USER1, create_test_create_bug_payload(cls.project.id))
        cls.bug_to_update = run_async(bug_to_update_future)
        cls.change_update_bug = run_async(change_update_bug_future)

    def test_error_when_missing_auth_header(self):
        # Given
        evt = create_event()

        # When
        rsp = update_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_missing_project_id(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context('user'))

        # When
        rsp = update_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required pathParameters parameter "bugId" in request')
        )

    def test_error_when_empty_payload(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'bugId': self.bug_to_update.id},
            body=UpdateBugPayload().api_dict()
        )

        # When
        rsp = update_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('No changes provided in update payload')
        )

    def test_error_when_bug_not_found(self):
        # Given
        bug_id = 'does_not_exist'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context('user'),
            path={'bugId': bug_id},
            body=UpdateBugPayload(title='title update').api_dict()
        )

        # When
        rsp = update_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body(f'No bug found with id: "{bug_id}"')
        )

    def test_error_when_updates_match_existing_bug(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'bugId': self.change_update_bug.id},
            body=UpdateBugPayload(title=self.change_update_bug.title).api_dict()
        )

        # When
        rsp = update_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('All changes in payload matches the existing record')
        )

    def test_error_when_user_lacks_permission_to_update(self):
        # Given
        user = 'user_lacks_access'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(user),
            path={'bugId': self.bug_to_update.id},
            body=UpdateBugPayload(title='some_edit').api_dict()
        )

        # When
        rsp = update_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.FORBIDDEN_STATUS,
            message_body(f'{user} does not have permission to read project {self.project.id}')
        )

    def test_user_updates_bug(self):
        # Given
        new_title = 'new_title'
        bug_before_update = self.bug_to_update
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'bugId': self.bug_to_update.id},
            body=UpdateBugPayload(title=new_title).api_dict()
        )

        # When
        rsp = update_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.OK_STATUS)
        assert json.loads(rsp['body'])['projectId'] is not None
        bug = json.loads(rsp['body'])['bug']
        assert_dict_attributes_equals(
            bug,
            {
                'id': bug_before_update.id,
                'createdOn': to_utc_str(bug_before_update.created_on),
                'title': new_title,
                'description': bug_before_update.description,
                'tags': bug_before_update.tags,
                'resolved': None
            }
        )


class TestResolveBug(TestCase):
    TEST_NAME = 'ResolveBug'
    USER1 = f'{TEST_NAME}_USER1'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        project_future = create_project(
            TestResolveBug.USER1,
            create_test_create_project_payload()
        )
        cls.project = run_async(project_future)

        bug_to_resolve_future = create_project_bug(cls.USER1, create_test_create_bug_payload(cls.project.id))
        resolved_bug_future = create_project_bug(cls.USER1, create_test_create_bug_payload(cls.project.id))

        cls.bug_to_resolve = run_async(bug_to_resolve_future)

        resolved_bug = run_async(resolved_bug_future)
        resolved_bug_future = resolve_project_bug(cls.USER1, resolved_bug.id)
        cls.resolved_bug = run_async(resolved_bug_future)[1]

    def test_error_when_missing_auth_header(self):
        # Given
        evt = create_event()

        # When
        rsp = resolve_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_no_bug_id(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context('user'))

        # When
        rsp = resolve_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required pathParameters parameter "bugId" in request')
        )

    def test_error_when_bug_not_found(self):
        # Given
        bug_id = 'does_not_exist'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context('user'),
            path={'bugId': bug_id}
        )

        # When
        rsp = resolve_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.NOT_FOUND_STATUS,
            message_body(f'No bug found with id: "{bug_id}"')
        )

    def test_error_when_user_lacks_access(self):
        # Given
        user = 'lacks_access_user'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(user),
            path={'bugId': self.bug_to_resolve.id}
        )

        # When
        rsp = resolve_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.FORBIDDEN_STATUS,
            message_body(f'{user} does not have permission to read project {self.project.id}')
        )

    def test_error_when_resolving_already_resolved_bug(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'bugId': self.resolved_bug.id}
        )

        # When
        rsp = resolve_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body(
                f'Bug {self.resolved_bug.id} has already been resolved by {self.resolved_bug.resolved.resolver_id} '
                f'on {self.resolved_bug.resolved.resolved_on}'
            )
        )

    def test_user_resolves_bug(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'bugId': self.bug_to_resolve.id}
        )

        # When
        rsp = resolve_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.OK_STATUS)
        bug_resolution = BugResolution.parse_obj(json.loads(rsp['body'])['bug']['resolved'])
        assert bug_resolution.resolver_id == self.USER1
        assert bug_resolution.resolved_on is not None


class TestDeleteBug(TestCase):
    TEST_NAME = 'DeleteBug'
    USER1 = f'{TEST_NAME}_USER1'

    @classmethod
    @patch('bug_killer_app.access.datastore.project.TransactWrite', new=DummyTransactWrite)
    def setUpClass(cls):
        project_future = create_project(
            TestDeleteBug.USER1,
            create_test_create_project_payload()
        )
        cls.project = run_async(project_future)

        bug_to_delete_future = create_project_bug(cls.USER1, create_test_create_bug_payload(cls.project.id))
        cls.bug_to_delete = run_async(bug_to_delete_future)

    def test_error_when_missing_auth_header(self):
        # Given
        evt = create_event()

        # When
        rsp = delete_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.UNAUTHORIZED_STATUS, message_body('Missing authorization header value'))

    def test_error_when_bug_id_not_given(self):
        # Given
        evt = create_event(request_context=create_cognito_authorizer_request_context('user'))

        # When
        rsp = delete_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.BAD_REQUEST_STATUS,
            message_body('Missing required pathParameters parameter "bugId" in request')
        )

    def test_error_when_bug_not_found(self):
        # Given
        bug_id = 'Does not exist'
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'bugId': bug_id},
        )

        # When
        rsp = delete_bug_handler(evt, None)

        # Then
        assert_response(rsp, HttpStatusCodes.NOT_FOUND_STATUS, message_body(f'No bug found with id: "{bug_id}"'))

    def test_user_deletes_project(self):
        # Given
        evt = create_event(
            request_context=create_cognito_authorizer_request_context(self.USER1),
            path={'bugId': self.bug_to_delete.id},
        )

        # When
        rsp = delete_bug_handler(evt, None)

        # Then
        assert_response(
            rsp,
            HttpStatusCodes.OK_STATUS,
            BugResponse(project_id=self.project.id, bug=self.bug_to_delete).api_dict()
        )
