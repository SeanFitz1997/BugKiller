import arrow

from bug_killer_schemas.models.bug import BugResolution, Bug


def test_bug_resolution():
    expected_data_dict = {
        'resolverId': '123',
        'resolvedOn': '2022-01-01T00:00:00Z',
    }
    resolution = BugResolution('123', arrow.get('2022-01-01'))

    assert resolution.to_dict() == expected_data_dict
    assert BugResolution.from_dict(expected_data_dict) == resolution


def test_bug():
    resolution = BugResolution('user_123', arrow.get('2022-01-01'))

    expected_data_dict = {
        'id': '123',
        'title': 'test title',
        'description': 'test description',
        'createdOn': '2022-01-01T00:00:00Z',
        'lastUpdatedOn': '2022-01-01T00:00:00Z',
        'tags': ['T1', 'T2'],
        'resolved': resolution.to_dict()
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

    assert bug.to_dict() == expected_data_dict
    assert Bug.from_dict(expected_data_dict) == bug
