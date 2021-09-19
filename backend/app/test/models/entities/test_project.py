from bug_killer.datastore.project_table.project_item import ProjectItem
from bug_killer.models.entities.project import Project
from bug_killer.util.entity import remove_prefix
from test.test_doubles.db_items import (
    create_test_bug_item,
    create_test_manager_item,
    create_test_member_item,
    create_test_project_item
)


mock_project_item = create_test_project_item()
mock_manager_item = create_test_manager_item()
mock_member_item = create_test_member_item()
mock_bug_item = create_test_bug_item()


def test_project_from_db_items_just_project_items():
    project = Project.from_db_items(mock_project_item)

    assert project.id == mock_project_item.project_id
    assert project.title == mock_project_item.title
    assert project.description == mock_project_item.description
    assert project.tags == mock_project_item.tags
    assert project.manager is None
    assert project.members is None
    assert project.bugs is None


def test_project_from_db_items_all_items():
    project = Project.from_db_items(
        mock_project_item, mock_manager_item, [mock_member_item], [mock_bug_item]
    )

    assert project.id == mock_project_item.project_id
    assert project.title == mock_project_item.title
    assert project.description == mock_project_item.description
    assert project.tags == mock_project_item.tags

    assert project.manager == remove_prefix(
        ProjectItem.MANAGER_SK_PREFIX, mock_manager_item.project_bug_manager_member_id
    )

    assert len(project.members) == 1
    assert project.members[0] == remove_prefix(
        ProjectItem.MEMBER_SK_PREFIX, mock_member_item.project_bug_manager_member_id
    )

    assert len(project.bugs) == 1
    assert project.bugs[0].id == remove_prefix(
        ProjectItem.BUG_SK_PREFIX, mock_bug_item.project_bug_manager_member_id
    )


def test_project_to_db_items():
    project = Project.from_db_items(mock_project_item)

    project_item, manager_item, member_items, bugs_items = project.to_db_items()

    assert project_item.project_id == mock_project_item.project_id
    assert manager_item is None
    assert member_items is None
    assert bugs_items is None


def test_project_to_db_items_all_items():
    project = Project.from_db_items(
        mock_project_item, mock_manager_item, [mock_member_item], [mock_bug_item]
    )

    project_item, manager_item, member_items, bugs_items = project.to_db_items()

    assert project_item.project_id == mock_project_item.project_id
    assert (
            manager_item.project_bug_manager_member_id
            == mock_manager_item.project_bug_manager_member_id
    )

    assert len(member_items) == 1
    assert (
            member_items[0].project_bug_manager_member_id
            == mock_member_item.project_bug_manager_member_id
    )

    assert len(bugs_items) == 1
    assert (
            bugs_items[0].project_bug_manager_member_id
            == mock_bug_item.project_bug_manager_member_id
    )
