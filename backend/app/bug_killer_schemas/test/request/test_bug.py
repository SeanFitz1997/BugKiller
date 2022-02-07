from bug_killer_schemas.request.bug import CreateBugPayload, UpdateBugPayload


def test_create_bug_payload():
    expected_data_dict = {
        'projectId': '123',
        'title': 'test title',
        'description': 'test desc',
        'tags': ['T1', 'T2']
    }
    payload = CreateBugPayload(
        project_id='123',
        title='test title',
        description='test desc',
        tags=['T2', 'T2', 'T1']
    )

    assert payload.api_dict() == expected_data_dict
    assert CreateBugPayload.parse_raw(payload.json()) == payload


def test_update_bug_payload():
    expected_data_dict = {
        'title': None,
        'description': None,
        'tags': ['T1', 'T2']
    }
    payload = UpdateBugPayload(tags=['T2', 'T2', 'T1'])

    assert payload.api_dict() == expected_data_dict
    assert UpdateBugPayload.parse_raw(payload.json()) == payload
