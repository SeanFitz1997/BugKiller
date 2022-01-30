from bug_killer_app.domain.request import ParameterType, get_body_param, get_path_param, get_header_param, \
    get_query_param


def test_get_body_param():
    evt = {ParameterType.BODY.value: {'test': 'value'}}
    assert get_body_param(evt, 'test') == 'value'


def test_get_path_param():
    evt = {ParameterType.PATH.value: {'test': 'value'}}
    assert get_path_param(evt, 'test') == 'value'


def test_get_header_param():
    evt = {ParameterType.HEADERS.value: {'test': 'value'}}
    assert get_header_param(evt, 'test') == 'value'


def test_get_query_param():
    evt = {ParameterType.QUERY.value: {'test': 'value'}}
    assert get_query_param(evt, 'test') == 'value'
