from unittest.mock import patch, MagicMock

from bug_killer_client.service.project import get_user_projects, get_project, create_project, update_project, \
    delete_project
from bug_killer_client.tests.helpers import create_mock_response, assert_expected_network_call
from bug_killer_client.util import get_auth_headers
from bug_killer_schemas.entities.project import Project
from bug_killer_schemas.request.project import UpdateProjectPayload, CreateProjectPayload
from bug_killer_schemas.response.project import UserProjectsResponse, ProjectResponse
from bug_killer_utils.function import run_async


token = 'token'
project_id = '123'


@patch('bug_killer_client.network.project.requests')
def test_get_user_projects(mock_requests):
    # Given
    expected_rsp = UserProjectsResponse.test_double()
    mock_get = MagicMock(return_value=create_mock_response(200, expected_rsp.api_dict()))
    mock_requests.get = mock_get

    # When
    rsp = run_async(get_user_projects(token))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(mock_get, '/projects', expected_headers=get_auth_headers(token))


@patch('bug_killer_client.network.project.requests')
def test_get_project(mock_requests):
    # Given
    project = Project.test_double(project_id=project_id)
    expected_rsp = ProjectResponse.test_double(project=project)
    mock_get = MagicMock(return_value=create_mock_response(200, expected_rsp.api_dict()))
    mock_requests.get = mock_get

    # When
    rsp = run_async(get_project(token, project_id))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(mock_get, f'/projects/{project_id}', expected_headers=get_auth_headers(token))


@patch('bug_killer_client.network.project.requests')
def test_create_project(mock_requests):
    # Given
    payload = CreateProjectPayload.test_double()
    expected_rsp = ProjectResponse.test_double()
    mock_post = MagicMock(return_value=create_mock_response(201, expected_rsp.api_dict()))
    mock_requests.post = mock_post

    # When
    rsp = run_async(create_project(token, payload))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(
        mock_post, f'/projects', expected_headers=get_auth_headers(token), expected_body=payload.api_dict())


@patch('bug_killer_client.network.project.requests')
def test_update_project(mock_requests):
    # Given
    payload = UpdateProjectPayload(title='test update')
    project = Project.test_double(project_id=project_id)
    expected_rsp = ProjectResponse(project=project)
    mock_patch = MagicMock(return_value=create_mock_response(200, expected_rsp.api_dict()))
    mock_requests.patch = mock_patch

    # When
    rsp = run_async(update_project(token, project_id, payload))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(
        mock_patch,
        f'/projects/{project_id}',
        expected_headers=get_auth_headers(token),
        expected_body=payload.api_dict()
    )


@patch('bug_killer_client.network.project.requests')
def test_delete_project(mock_requests):
    # Given
    project = Project.test_double(project_id=project_id)
    expected_rsp = ProjectResponse.test_double(project=project)
    mock_delete = MagicMock(return_value=create_mock_response(200, expected_rsp.api_dict()))
    mock_requests.delete = mock_delete

    # When
    rsp = run_async(delete_project(token, project_id))

    # Then
    assert rsp == expected_rsp
    assert_expected_network_call(mock_delete, f'/projects/{project_id}', expected_headers=get_auth_headers(token))
