import arrow

from bug_killer_schemas.models.bug import Bug
from bug_killer_schemas.response.bug import BugResponse


def test_bug_response():
    bug = Bug(
        id='123',
        title='test title',
        description='test description',
        created_on=arrow.get('2022-01-01'),
        last_updated_on=arrow.get('2022-01-01'),
        tags=['T2', 'T2', 'T1'],
    )

    expected_rsp_dict = {
        'projectId': '123',
        'bug': bug.api_dict()
    }

    rsp = BugResponse(project_id='123', bug=bug)

    assert rsp.api_dict() == expected_rsp_dict
    assert BugResponse.parse_raw(rsp.json()) == rsp
