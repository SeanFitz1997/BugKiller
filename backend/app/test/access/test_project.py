from unittest.mock import patch

from pynamodb.exceptions import DoesNotExist

from bug_killer.access.project import get_project_by_id
from bug_killer.models.project import Project
from test.test_doubles.bug import create_test_bug
from test.test_doubles.project_item import create_test_project_item


mock_project_id = '123'
mock_project_item = create_test_project_item(mock_project_id)
mock_bugs = [
    create_test_bug('abc'),
    create_test_bug('dfg'),
]

x = DoesNotExist


@patch('bug_killer.access.project.get_project_item_by_id', lambda *args: mock_project_item)
def test_get_project_by_id():
    project = get_project_by_id(mock_project_id)

    assert isinstance(project, Project)
    assert project.bugs is None
    assert project.manager is None
    assert project.team is None


@patch('bug_killer.access.project.get_project_item_by_id', lambda *args: mock_project_item)
@patch('bug_killer.access.project.get_bugs_by_project_id', lambda *args: mock_bugs)
def test_get_project_by_id_with_bugs():
    project = get_project_by_id(mock_project_id, with_bugs=True)

    assert isinstance(project, Project)
    assert project.bugs == mock_bugs


@patch('bug_killer.access.project.get_project_item_by_id')
def test_get_project_not_found(mock_get_project_item_by_id):
    mock_get_project_item_by_id.side_effect = DoesNotExist()

    assert get_project_by_id(mock_project_id) is None
