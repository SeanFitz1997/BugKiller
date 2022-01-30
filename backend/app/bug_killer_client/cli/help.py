from typing import Optional, Dict, List, Tuple, NoReturn, Any

from bug_killer_utils.collections import is_dict_empty


class OperationHelpDetails:

    def __init__(self, operation_help: Optional[str] = None, arguments_help: Optional[Dict[str, str]] = None):
        self.operation_help = operation_help
        self.arguments_help = arguments_help or {}

    def __repr__(self) -> str:
        return str(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        return {
            'operationHelp': self.operation_help,
            'argumentsHelp': self.arguments_help
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OperationHelpDetails':
        return OperationHelpDetails(
            operation_help=data.get('operationHelp'),
            arguments_help=data.get('argumentsHelp')
        )

    @staticmethod
    def from_doc_str(doc: str) -> 'OperationHelpDetails':
        if not doc:
            return OperationHelpDetails()

        # Filter out empty lines
        lines = doc.split('\n')
        lines = [line.strip() for line in lines if line.strip()]

        # Get command and args
        command_lines, arg_lines = OperationHelpDetails._get_command_and_arg_lines(lines)
        command_help = ' '.join(command_lines)
        arg_helps = OperationHelpDetails._get_arg_helps(arg_lines)

        return OperationHelpDetails(
            operation_help=command_help or None,
            arguments_help=arg_helps if not is_dict_empty(arg_helps) else None
        )

    @staticmethod
    def _get_command_and_arg_lines(lines: List[str]) -> Tuple[List[str], List[str]]:
        #   arg lines are in the form <arg name>: <arg decs>
        #   All lines prior to ':' are command lines and the rest are arg lines
        arg_index = next((i for i, x in enumerate(lines) if ':' in x), len(lines))
        command_lines = lines[:arg_index]
        arg_lines = lines[arg_index:]

        return command_lines, arg_lines

    @staticmethod
    def _get_arg_helps(arg_lines: List[str]) -> Dict[str, str]:
        arg_helps = {}
        arg_name = None
        arg_help_accumulation = []

        for line in arg_lines:
            if ':' in line:
                if arg_name and arg_help_accumulation:
                    OperationHelpDetails._add_arg_help(arg_helps, arg_name, arg_help_accumulation)

                arg_name, arg_desc = line.split(':')
                arg_help_accumulation.append(arg_desc)

        OperationHelpDetails._add_arg_help(arg_helps, arg_name, arg_help_accumulation)

        return arg_helps

    @staticmethod
    def _add_arg_help(arg_helps: Dict[str, str], arg_name: Optional[str], arg_desc_lines: List[str]) -> NoReturn:
        if arg_name and arg_desc_lines:
            arg_desc = ' '.join(arg_desc_lines).strip()
            if not arg_desc:
                raise ValueError(f'Empty description for arg: {arg_name}')

            arg_helps[arg_name] = arg_desc
            arg_desc_lines.clear()
