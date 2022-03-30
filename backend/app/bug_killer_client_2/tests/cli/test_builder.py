import json
from typing import NoReturn
from unittest import TestCase

import pytest

from bug_killer_api_interface.schemas.request.project import UpdateProjectPayload
from bug_killer_client.cli.builder import get_cli_defaults, generate_cli


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
        cls.default_model_value = UpdateProjectPayload()
        cls.test_defaults = {'modelValue': cls.default_model_value.json()}
        cls.test_title = 'Test CLI'

    def test_generate_cli_error_when_no_operations(self):
        with pytest.raises(ValueError):
            generate_cli([])

    def test_generate_cli_with_operation(self):
        # Given
        str_param = 'test'
        model_param = UpdateProjectPayload(title='a test value')

        # When
        parser = generate_cli([self.test_operation], self.test_defaults, self.test_title)

        # Then
        assert parser.description == self.test_title

        # Fails if no args given
        with pytest.raises(SystemExit):
            parser.parse_args([])

        # Fails if command not recognised
        with pytest.raises(SystemExit):
            parser.parse_args(['wrong_command'])

        # Fails if required params not given
        with pytest.raises(SystemExit):
            parser.parse_args(['testOperation'])

        # Passes if all args given
        result = parser.parse_args(['testOperation', '--strValue', str_param, '--modelValue', model_param.json()])
        assert result.operation == 'testOperation'
        assert result.strValue == str_param
        assert result.modelValue == model_param
        assert result.verbose is False

        # Pass if all required args given
        result = parser.parse_args(['testOperation', '--strValue', str_param])
        assert result.strValue == str_param
        assert result.modelValue == self.default_model_value
