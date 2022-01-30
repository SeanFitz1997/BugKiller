import arrow

from bug_killer_app.datastore.project_table.project_item import ProjectItem, ProjectAssociationPrefix
from bug_killer_app.models.bug import BkAppBug
from bug_killer_app.models.project import BkAppProject
from bug_killer_app.test.test_doubles.db_items import (
    create_test_project_item, create_test_manager_item, create_test_member_item, create_test_bug_item
)
from bug_killer_app.test.test_doubles.entities import create_test_project


def test_project_from_db_items():
    # Given
    project_id = 'p1'
    bug_id = 'b1'
    manager_id = 'ma1'
    member_id = 'me1'
    dt = arrow.get('2022-01-01')

    project_item = create_test_project_item(project_id, created_on=dt, last_updated_on=dt)
    bug_item = create_test_bug_item(project_id, bug_id, created_on=dt, last_updated_on=dt)
    manager_item = create_test_manager_item(project_item.project_id, manager_id)
    member_item = create_test_member_item(project_item.project_id, member_id)

    # When
    project = BkAppProject.from_db_items(project_item, manager_item, [member_item], [bug_item])

    # Then
    assert project == BkAppProject(
        id=project_id,
        title=project_item.title,
        description=project_item.description,
        manager=manager_id,
        created_on=dt,
        last_updated_on=dt,
        tags=project_item.tags,
        members=[member_id],
        bugs=[
            BkAppBug(
                id=bug_id,
                title=bug_item.title,
                description=bug_item.description,
                tags=bug_item.tags,
                created_on=dt,
                last_updated_on=dt,
            )
        ]
    )


def test_project_to_db_items():
    # Given
    dt = arrow.get('2022-01-01')
    project = create_test_project(created_on=dt, last_updated_on=dt)

    # When
    project_item, manager_item, member_items, bugs_items = project.to_db_items()

    # Then
    assert project_item.to_json() == ProjectItem(
        project_id=project.id,
        project_association=ProjectAssociationPrefix.PROJECT.value + project.id,
        title=project.title,
        description=project.description,
        tags=project.tags,
        created_on=project.created_on,
        last_updated_on=project.last_updated_on,
    ).to_json()

    assert manager_item.to_json() == ProjectItem(
        project_id=project.id,
        project_association=ProjectAssociationPrefix.MANAGER.value + project.manager
    ).to_json()

    assert len(member_items) == len(project.members) == 1
    assert member_items[0].to_json() == ProjectItem(
        project_id=project.id,
        project_association=ProjectAssociationPrefix.MEMBER.value + project.members[0]
    ).to_json()

    assert len(bugs_items) == len(project.bugs) == 1
    assert bugs_items[0].to_json() == ProjectItem(
        project_id=project.id,
        project_association=ProjectAssociationPrefix.BUG.value + project.bugs[0].id,
        title=project.bugs[0].title,
        description=project.bugs[0].description,
        tags=project.bugs[0].tags,
        created_on=project.bugs[0].created_on,
        last_updated_on=project.bugs[0].last_updated_on,
    ).to_json()
