import arrow

from bug_killer_app.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute
from bug_killer_app.models.bug_resolution import BkAppBugResolution
from bug_killer_app.test.test_doubles.db_items import create_test_bug_resolution_attribute
from bug_killer_app.test.test_doubles.entities import create_test_bug_resolution


def test_bug_resolution_from_db_attribute():
    # Given
    dt = arrow.utcnow()
    resolution_attr = create_test_bug_resolution_attribute()

    # When
    resolution = BkAppBugResolution.from_db_attribute(resolution_attr)

    # Then
    assert resolution == BkAppBugResolution(
        resolver_id=resolution_attr.resolver_id,
        resolved_on=dt
    )


def test_bug_resolution_to_db_attribute():
    # Given
    dt = arrow.utcnow()
    resolution = create_test_bug_resolution()

    # When
    resolution_attr = resolution.to_db_attribute()

    # Then
    assert resolution_attr.as_dict() == BugResolutionMapAttribute(
        resolver_id=resolution.resolver_id,
        resolved_on=resolution.resolved_on
    ).as_dict()
