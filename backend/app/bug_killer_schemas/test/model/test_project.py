import arrow

from bug_killer_schemas.models.bug import BugResolution, Bug
from bug_killer_schemas.models.project import Project


def test_project():
    resolution = BugResolution('user_123', arrow.get('2022-01-01'))
    bug = Bug(
        id='123',
        title='test title',
        description='test description',
        created_on=arrow.get('2022-01-01'),
        last_updated_on=arrow.get('2022-01-01'),
        tags=['T2', 'T2', 'T1'],
        resolved=resolution
    )

    expected_project_dict = {
        'id': '123',
        'title': 'test project',
        'description': 'this is a test project',
        'manager': 'M1',
        'createdOn': '2022-01-01T00:00:00Z',
        'lastUpdatedOn': '2022-01-01T00:00:00Z',
        'tags': ['T1', 'T2'],
        'members': ['M1', 'M2'],
        'bugs': [bug.to_dict()]
    }

    project = Project(
        id='123',
        title='test project',
        description='this is a test project',
        manager='M1',
        created_on=arrow.get('2022-01-01'),
        last_updated_on=arrow.get('2022-01-01'),
        tags=['T2', 'T2', 'T1'],
        members=['M2', 'M2', 'M1'],
        bugs=[bug]
    )

    assert project.to_dict() == expected_project_dict
    assert Project.from_dict(expected_project_dict) == project
