import json
from unittest import TestCase

from bug_killer_client.cli.help import OperationHelpDetails


class TestOperationHelpDetails(TestCase):

    def test_operation_help_details_constructor(self):
        # Given
        operation_desc = 'test_operation'
        arg_desc = {'testParam': 'param_desc'}
        expected_data = {
            'operationHelp': operation_desc,
            'argumentsHelp': arg_desc
        }

        # When
        docs = OperationHelpDetails(operation_help=operation_desc, arguments_help=arg_desc)

        # Then
        assert docs.api_dict() == expected_data
        assert OperationHelpDetails.parse_raw(json.dumps(expected_data))

    def test_operation_help_details_no_docs(self):
        assert OperationHelpDetails.from_doc_str(None) == OperationHelpDetails()

    def test_operation_help_details_just_command_desc(self):
        # Given
        just_command_doc = 'just_command'

        # When
        docs = OperationHelpDetails.from_doc_str(just_command_doc)

        # Then
        assert docs == OperationHelpDetails(operation_help=just_command_doc)

    def test_operation_help_details(self):
        # Given
        command_desc = 'command_desc'
        arg_desc = {f'arg{i}': f'arg{i}_desc' for i in range(2)}
        doc_str = f'{command_desc}\n'
        for arg_k, arg_v in arg_desc.items():
            doc_str += f'{arg_k}: {arg_v}\n'

        # When
        doc = OperationHelpDetails.from_doc_str(doc_str)

        # Then
        assert doc == OperationHelpDetails(operation_help=command_desc, arguments_help=arg_desc)
