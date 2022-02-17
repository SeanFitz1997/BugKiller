from argparse import Namespace
from unittest import TestCase
from unittest.mock import patch, MagicMock

from bug_killer_client.cli.executor import execute_operation
from bug_killer_schemas.request.project import UpdateProjectPayload


async def mock_operation(test_param: str):
    return UpdateProjectPayload(title=test_param)


class TestExecutor(TestCase):

    @patch('bug_killer_client.cli.executor.logging')
    def test_execute_operation_sets_logging(self, mock_logging):
        # Given
        mock_default_logger = MagicMock()
        mock_logging.getLogger = MagicMock(return_value=mock_default_logger)
        # mock_default_logger.setLevel = MagicMock()

        # When
        cli_args = Namespace(operation='mockOperation', testParam='test', verbose=True)
        execute_operation([mock_operation], cli_args)

        # Then
        mock_logging.getLogger().setLevel.assert_called_once_with(mock_logging.INFO)

    def test_execute_operation(self):
        # When
        test_param = 'test'
        cli_args = Namespace(operation='mockOperation', testParam=test_param, verbose=False)
        result = execute_operation([mock_operation], cli_args)

        # Then
        assert result == UpdateProjectPayload(title=test_param)
