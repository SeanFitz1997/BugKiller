from bug_killer_api_interface.schemas.request.project import CreateProjectPayload, UpdateProjectPayload


def test_create_project():
    expected_data_dict = {
        'title': 'test title',
        'description': 'test desc',
        'members': ['M1', 'M2'],
        'tags': ['T1', 'T2']
    }
    payload = CreateProjectPayload(
        title='test title',
        description='test desc',
        members=['M2', 'M2', 'M1'],
        tags=['T2', 'T2', 'T1']
    )

    assert payload.api_dict() == expected_data_dict
    assert CreateProjectPayload.parse_raw(payload.json()) == payload


def test_update_project():
    expected_data_dict = {
        'title': None,
        'description': None,
        'manager': None,
        'members': ['M1', 'M2'],
        'tags': None
    }
    payload = UpdateProjectPayload(members=['M2', 'M2', 'M1'])

    assert payload.api_dict() == expected_data_dict
    assert UpdateProjectPayload.parse_raw(payload.json()) == payload
