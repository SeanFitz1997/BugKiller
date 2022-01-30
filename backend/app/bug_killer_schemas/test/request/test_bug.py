from bug_killer_schemas.request.bug import CreateBugPayload, UpdateBugPayload


def test_create_bug_payload():
    expected_data_dict = {
        'projectId': '123',
        'title': 'test title',
        'description': 'test desc',
        'tags': ['T1', 'T2']
    }
    payload = CreateBugPayload('123', 'test title', 'test desc', ['T2', 'T2', 'T1'])

    assert payload.to_dict() == expected_data_dict
    assert CreateBugPayload.from_dict(expected_data_dict) == payload


def test_update_bug_payload():
    expected_data_dict = {
        'title': None,
        'description': None,
        'tags': ['T1', 'T2']
    }
    payload = UpdateBugPayload(tags=['T2', 'T2', 'T1'])

    assert payload.to_dict() == expected_data_dict
    assert UpdateBugPayload.from_dict(expected_data_dict) == payload
