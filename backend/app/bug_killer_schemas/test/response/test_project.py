import arrow

from bug_killer_schemas.models.project import Project
from bug_killer_schemas.response.project import UserProjectsResponse, ProjectResponse


def test_user_project_response():
    manager_project = Project(
        id='123',
        title='test manager project',
        description='this is a test project',
        manager='M1',
        created_on=arrow.get('2022-01-01'),
        last_updated_on=arrow.get('2022-01-01')
    )
    member_project = Project(
        id='123',
        title='test member project',
        description='this is a test project',
        manager='M1',
        created_on=arrow.get('2022-01-01'),
        last_updated_on=arrow.get('2022-01-01')
    )

    expected_response_dict = {
        'managerProjects': [manager_project.to_dict()],
        'memberProjects': [member_project.to_dict()]
    }

    rsp = UserProjectsResponse([manager_project], [member_project])

    assert rsp.to_dict() == expected_response_dict
    assert UserProjectsResponse.from_dict(expected_response_dict) == rsp


def test_project_response():
    project = Project(
        id='123',
        title='test project',
        description='this is a test project',
        manager='M1',
        created_on=arrow.get('2022-01-01'),
        last_updated_on=arrow.get('2022-01-01')
    )

    expected_rsp_dict = {'project': project.to_dict()}

    rsp = ProjectResponse(project)

    assert rsp.to_dict() == expected_rsp_dict
    assert ProjectResponse.from_dict(expected_rsp_dict) == rsp
