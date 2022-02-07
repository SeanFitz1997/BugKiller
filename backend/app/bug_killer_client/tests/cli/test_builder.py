import json
from typing import NoReturn
from unittest import TestCase

import pytest

from bug_killer_client.cli.builder import get_cli_defaults, generate_cli
from bug_killer_schemas.request.project import UpdateProjectPayload


def test_get_cli_defaults_no_file():
    assert get_cli_defaults('does_not_exist') is None


def test_get_cli_defaults_with_file(tmpdir):
    # Given
    expected_settings = {'some': 'value'}
    path = tmpdir / 'settings.json'
    path.write(json.dumps(expected_settings))

    # When, Then
    assert get_cli_defaults(path) == expected_settings


class TestGenerateCli(TestCase):

    @classmethod
    def setUpClass(cls):
        def test_operation(value_with_default: int, str_value: str, model_value: UpdateProjectPayload) -> NoReturn:
            """
            A test operation for cli
            str_value: A test str value
            model_value: A test model value
            """
            pass

        cls.test_operation = test_operation
        cls.test_defaults = {'valueWithDefault': 1}
        cls.test_title = 'Test CLI'

    def test_generate_cli_error_when_no_operations(self):
        with pytest.raises(ValueError):
            generate_cli([])

    def test_generate_cli_with_operation(self):
        # TODO: Finish test
        parser = generate_cli([self.test_operation], self.test_defaults, self.test_title)

        assert parser.description == self.test_title
