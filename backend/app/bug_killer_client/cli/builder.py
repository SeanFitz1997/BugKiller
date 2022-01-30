import json
from argparse import ArgumentParser
from functools import partial
from inspect import signature
from typing import Callable, List, Any, Union, Dict, Optional

from bug_killer_client.cli.help import OperationHelpDetails
from bug_killer_utils.strings import snake_case_to_camel_case


def generate_cli(
        operations: List[Callable],
        saved_defaults: Optional[Dict[str, str]] = None,
        cli_title: Optional[str] = None
) -> ArgumentParser:
    """
    Dynamically creates a CLI from with a command for each operation.
    Help info for each operation and its arguments be retrieved from the function doc string
    operations: List of functions to create a CLI command for.
    saved_defaults: Values to use as default for the CLI commands
    cli_title: The title to given to the CLI
    """
    saved_defaults = saved_defaults or {}

    # Create parent parser
    parser = ArgumentParser(description=cli_title)
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Includes INFO logs to operation execution')
    sub_parsers = parser.add_subparsers(dest='operation', required=True)

    for function in operations:
        # Attempt to receive help info from the doc string
        operation_help = OperationHelpDetails.from_doc_str(function.__doc__)

        # Create a sub parser for the operation
        function_signature = signature(function)
        sub_parser = sub_parsers.add_parser(
            snake_case_to_camel_case(function.__name__),
            help=operation_help.operation_help
        )

        for param in function_signature.parameters.values():
            # Add an option for each of the functions args
            sub_parser.add_argument(
                f'--{snake_case_to_camel_case(param.name)}',
                type=_get_arg_type(param.annotation),
                required=param.name not in saved_defaults,
                help=operation_help.arguments_help.get(param.name)
            )

    return parser


def _resolve_object_from_dict_str(cls: type, data: str) -> Any:
    data_dict = json.loads(data)
    return cls.from_dict(data_dict)


def _get_arg_type(cls: type) -> Union[type, Callable[[str], Any]]:
    if cls is str:
        return None
    elif cls in [int, float, bool]:
        return cls
    return partial(_resolve_object_from_dict_str, cls)
