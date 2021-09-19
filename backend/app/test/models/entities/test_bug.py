from bug_killer.datastore.project_table.project_item import ProjectItem
from bug_killer.models.entities.bug import Bug
from bug_killer.util.entity import remove_prefix
from test.test_doubles.db_items import create_test_bug_item
from test.test_doubles.entities import create_test_bug, create_test_resolution


mock_bug = create_test_bug()
mock_resolution = create_test_resolution()


def test_bug_from_db_item():
    mock_bug_item = create_test_bug_item()
    bug = Bug.from_db_item(mock_bug_item)

    assert bug.id == remove_prefix(
        ProjectItem.BUG_SK_PREFIX, mock_bug_item.project_bug_manager_member_id
    )
    assert bug.title == mock_bug_item.title
    assert bug.description == mock_bug_item.description
    assert bug.tags == mock_bug_item.tags
    assert bug.created_on == mock_bug_item.created_on
    assert bug.last_updated_on == mock_bug_item.last_updated_on
    assert bug.resolved is not None
