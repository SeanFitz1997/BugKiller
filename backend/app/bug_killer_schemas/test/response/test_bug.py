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
        'bug': bug.to_dict()
    }

    rsp = BugResponse('123', bug)

    assert rsp.to_dict() == expected_rsp_dict
    assert BugResponse.from_dict(expected_rsp_dict) == rsp
