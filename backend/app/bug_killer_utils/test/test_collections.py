import pytest

from bug_killer_utils.collections import flatten, add_to_dict_if_exists, is_jsonable, is_dict_empty, \
    remove_none_values_from_dict, remove_duplicates_in_list, keys_to_camel_case, keys_to_snake_case


@pytest.mark.parametrize('lst, expected', [
    ([[], [], [[], []]], []),
    ([[1, 2], [[3, 4], [5, 6]]], [1, 2, 3, 4, 5, 6])
])
def test_flatten(lst, expected):
    assert flatten(lst) == expected


@pytest.mark.parametrize('added_value, is_added', [
    (None, False),
    ('value', True)
])
def test_add_to_dict_if_exists(added_value, is_added):
    data = {}
    add_to_dict_if_exists(data, 'test', added_value)
    assert ('test' in data) is is_added


@pytest.mark.parametrize('data, expected', [
    ({'test': 'value'}, True),
    ({'test': {'set is not jsonable'}}, False)
])
def test_is_jsonable(data, expected):
    assert is_jsonable(data) is expected


@pytest.mark.parametrize('data, expected', [
    ({}, True),
    ({'test': None}, True),
    ({'test': 'value'}, False)
])
def test_is_dict_empty(data, expected):
    assert is_dict_empty(data) is expected


@pytest.mark.parametrize('data, expected', [
    ({}, {}),
    ({'test': None}, {}),
    ({'test': 'value'}, {'test': 'value'})
])
def test_remove_none_values_from_dict(data, expected):
    assert remove_none_values_from_dict(data) == expected


@pytest.mark.parametrize('lst, expected', [
    ([], []),
    ([1, 1, 2], [1, 2]),
])
def test_remove_duplicates_in_list(lst, expected):
    assert remove_duplicates_in_list(lst) == expected


@pytest.mark.parametrize('string, expected', [
    ({'': None}, {'': None}),
    ({'test': None}, {'test': None}),
    ({'test_value': None}, {'testValue': None}),
])
def test_keys_to_camel_case(string, expected):
    assert keys_to_camel_case(string) == expected


@pytest.mark.parametrize('string, expected', [
    ({'': None}, {'': None}),
    ({'test': None}, {'test': None}),
    ({'testValue': None}, {'test_value': None}),
])
def test_keys_to_snake_case(string, expected):
    assert keys_to_snake_case(string) == expected
