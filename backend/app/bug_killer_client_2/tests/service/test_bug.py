from unittest.mock import patch, MagicMock

from bug_killer_api_interface.schemas.entities.bug import Bug
from bug_killer_api_interface.schemas.request import UpdateBugPayload, CreateBugPayload
from bug_killer_api_interface.schemas.response import BugResponse
from bug_killer_client.service.bug import get_bug, create_bug, update_bug, delete_bug
from bug_killer_client.tests.helpers import create_mock_response, assert_expected_network_call
from bug_killer_client.util import get_auth_headers
from bug_killer_utils.function import run_async


token = 'token'
bug_id = '123'


@patch('bug_killer_client.network.bug.requests')
def test_get_bug(mock_requests):
    # Given
    expected_rsp = BugResponse.test_double(bug=Bug.test_double(bug_id=bug_id))
    mock_get = MagicMock(return_value=create_mock_response(200, expected_rsp.api_dict()))
    mock_requests.get = mock_get

    # When
    rsp = run_async(get_bug(token, bug_id))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(mock_get, f'/bugs/{bug_id}', expected_headers=get_auth_headers(token))


@patch('bug_killer_client.network.bug.requests')
def test_create_bug(mock_requests):
    # Given
    payload = CreateBugPayload.test_double()
    expected_rsp = BugResponse.test_double(bug=Bug.test_double(bug_id=bug_id))
    mock_post = MagicMock(return_value=create_mock_response(201, expected_rsp.api_dict()))
    mock_requests.post = mock_post

    # When
    rsp = run_async(create_bug(token, payload))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(
        mock_post, f'/bugs',
        expected_headers=get_auth_headers(token), expected_body=payload.api_dict()
    )


@patch('bug_killer_client.network.bug.requests')
def test_update_bug(mock_requests):
    # Given
    payload = UpdateBugPayload(title='new title')
    expected_rsp = BugResponse.test_double(bug=Bug.test_double(bug_id=bug_id))
    mock_patch = MagicMock(return_value=create_mock_response(200, expected_rsp.api_dict()))
    mock_requests.patch = mock_patch

    # When
    rsp = run_async(update_bug(token, bug_id, payload))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(
        mock_patch, f'/bugs/{bug_id}',
        expected_headers=get_auth_headers(token), expected_body=payload.api_dict()
    )


@patch('bug_killer_client.network.bug.requests')
def test_resolve_bug(mock_requests):
    # Given
    payload = UpdateBugPayload(title='new title')
    expected_rsp = BugResponse.test_double(bug=Bug.test_double(bug_id=bug_id))
    mock_patch = MagicMock(return_value=create_mock_response(200, expected_rsp.api_dict()))
    mock_requests.patch = mock_patch

    # When
    rsp = run_async(update_bug(token, bug_id, payload))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(
        mock_patch, f'/bugs/{bug_id}',
        expected_headers=get_auth_headers(token), expected_body=payload.api_dict()
    )


@patch('bug_killer_client.network.bug.requests')
def test_delete_bug(mock_requests):
    # Given
    expected_rsp = BugResponse.test_double(bug=Bug.test_double(bug_id=bug_id))
    mock_delete = MagicMock(return_value=create_mock_response(200, expected_rsp.api_dict()))
    mock_requests.delete = mock_delete

    # When
    rsp = run_async(delete_bug(token, bug_id))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(mock_delete, f'/bugs/{bug_id}', expected_headers=get_auth_headers(token))
