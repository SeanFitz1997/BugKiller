from bug_killer.models.dto.project import CreateProjectPayload
from test.test_doubles.default_values import *


def create_test_create_project_payload(
        title: str = mock_project_title,
        description: str = mock_project_description,
        manager: str = mock_manager_id,
) -> CreateProjectPayload:
    return CreateProjectPayload(title=title, description=description, manager=manager)
