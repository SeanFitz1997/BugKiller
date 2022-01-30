from bug_killer_schemas.request.project import CreateProjectPayload, UpdateProjectPayload


def test_create_project():
    expected_data_dict = {
        'title': 'test title',
        'description': 'test desc',
        'members': ['M1', 'M2'],
        'tags': ['T1', 'T2']
    }
    payload = CreateProjectPayload('test title', 'test desc', ['M2', 'M2', 'M1'], ['T2', 'T2', 'T1'])

    assert payload.to_dict() == expected_data_dict
    assert CreateProjectPayload.from_dict(expected_data_dict) == payload


def test_update_project():
    expected_data_dict = {
        'title': None,
        'description': None,
        'manager': None,
        'members': ['M1', 'M2'],
        'tags': None
    }
    payload = UpdateProjectPayload(members=['M2', 'M2', 'M1'])

    assert payload.to_dict() == expected_data_dict
    assert UpdateProjectPayload.from_dict(expected_data_dict) == payload
