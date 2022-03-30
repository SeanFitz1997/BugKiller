import arrow

from bug_killer_api_interface.schemas.entities.bug import BugResolution, Bug


def test_bug_resolution():
    expected_data_dict = {
        'resolverId': '123',
        'resolvedOn': '2022-01-01T00:00:00Z',
    }
    resolution = BugResolution(resolver_id='123', resolved_on=arrow.get('2022-01-01'))

    assert resolution.api_dict() == expected_data_dict
    assert BugResolution.parse_raw(resolution.json()) == resolution


def test_bug():
    resolution = BugResolution(resolver_id='user_123', resolved_on=arrow.get('2022-01-01'))

    expected_data_dict = {
        'id': '123',
        'title': 'test title',
        'description': 'test description',
        'createdOn': '2022-01-01T00:00:00Z',
        'lastUpdatedOn': '2022-01-01T00:00:00Z',
        'tags': ['T1', 'T2'],
        'resolved': resolution.api_dict()
    }
    bug = Bug(
        id='123',
        title='test title',
        description='test description',
        created_on=arrow.get('2022-01-01'),
        last_updated_on=arrow.get('2022-01-01'),
        tags=['T2', 'T2', 'T1'],
        resolved=resolution
    )

    assert bug.api_dict() == expected_data_dict
    assert Bug.parse_raw(bug.json()) == bug
