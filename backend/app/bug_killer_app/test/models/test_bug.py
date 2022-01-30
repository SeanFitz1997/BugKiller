import arrow

from bug_killer_app.datastore.project_table.project_item import ProjectItem, ProjectAssociationPrefix
from bug_killer_app.models.bug import BkAppBug
from bug_killer_app.test.test_doubles.db_items import create_test_bug_item
from bug_killer_app.test.test_doubles.entities import create_test_bug, create_test_bug_resolution


def test_bug_from_db_item():
    # Given
    project_id = 'p1'
    bug_id = 'b1'
    dt = arrow.get('2022-01-01')
    bug_item = create_test_bug_item(project_id, bug_id, created_on=dt, last_updated_on=dt)

    # When
    bug = BkAppBug.from_db_item(bug_item)

    # Then
    assert bug == BkAppBug(
        id=bug_id,
        title=bug_item.title,
        description=bug_item.description,
        created_on=dt,
        last_updated_on=dt,
        tags=bug_item.tags,
    )


def test_bug_to_db_item():
    # Given
    project_id = 'p1'
    bug_id = 'b1'
    dt = arrow.get('2022-01-01')
    resolution = create_test_bug_resolution()
    bug = create_test_bug(bug_id, resolved=resolution, created_on=dt, last_updated_on=dt)

    # When
    bug_item = bug.to_db_item(project_id)

    # Then
    assert bug_item.to_json() == ProjectItem(
        project_id=project_id,
        project_association=ProjectAssociationPrefix.BUG.value + bug.id,
        title=bug.title,
        description=bug.description,
        tags=bug.tags,
        created_on=bug.created_on,
        last_updated_on=bug.last_updated_on,
        bug_resolution=resolution.to_db_attribute()
    ).to_json()
