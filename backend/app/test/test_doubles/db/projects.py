import arrow
import pytest

from bug_killer.datastore.project_table.project_item import ProjectItem
from bug_killer.util.collections import flatten
from test.test_doubles.entities import create_test_project, create_test_bug


user_with_projects = "user_with_projects"
user_without_projects = "user_without_projects"
user_with_delete_project = "user_with_delete_project"

# User with projects has 3 member projects and 1 manager project
manager_project = create_test_project(
    project_id="ManagerProject",
    manager=user_with_projects
)
member_projects = [
    create_test_project(
        project_id=f"MemberProject{i}",
        members=[user_with_projects],
        created_on=arrow.utcnow().shift(days=-i)
    )
    for i in range(3)
]

# Project that will be deleted
delete_to_project = create_test_project(project_id="DeleteProject")

# === API Test Items === #
api_project_to_update = create_test_project(manager='api_update_user', last_updated_on=arrow.utcnow().shift(hours=-1))
api_project_no_op_update = create_test_project(manager='api_update_user')

api_project_to_delete = create_test_project(manager='api_delete_user')

api_project_add_bug = create_test_project(manager='api_add_bug')

api_bug_to_delete = create_test_bug()
api_project_delete_bug = create_test_project(manager='api_delete_bug', bugs=[api_bug_to_delete])


@pytest.fixture(scope="session")
def populate_project_table_with_project_items(project_table):
    with ProjectItem.batch_write() as batch:
        projects_to_write = flatten([
            manager_project,
            member_projects,
            delete_to_project,
            api_project_to_update,
            api_project_no_op_update,
            api_project_to_delete,
            api_project_add_bug,
            api_project_delete_bug
        ])
        project_items = flatten([project.to_db_items() for project in projects_to_write])
        [batch.save(item) for item in project_items]
