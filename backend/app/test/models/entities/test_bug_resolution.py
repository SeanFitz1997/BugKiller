from bug_killer.models.entities.bug_resolution import BugResolution
from test.test_doubles.db_items import create_test_bug_resolution


def test_bug_resolution_from_db_attribute():
    mock_bug_resolution_attribute = create_test_bug_resolution()
    bug_resolution = BugResolution.from_db_attribute(mock_bug_resolution_attribute)

    assert bug_resolution.resolved_on == mock_bug_resolution_attribute.resolved_on
    assert bug_resolution.resolver_id == mock_bug_resolution_attribute.resolver_id
