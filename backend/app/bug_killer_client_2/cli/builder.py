import json
import os.path
from argparse import ArgumentParser
from functools import partial
from inspect import signature
from typing import Callable, List, Union, Type
from typing import Optional, Dict

from bug_killer_client.cli.help import OperationHelpDetails
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.strings import snake_case_to_camel_case


DEFAULT_DATA_PATH = os.path.join('data', 'cli_defaults.json')


def get_cli_defaults(path: Optional[str] = None) -> Optional[Dict[str, str]]:
    path = path or DEFAULT_DATA_PATH
    if os.path.exists(path):
        with open(path) as f:
            defaults = json.load(f)
            return defaults


def generate_cli(
        operations: List[Callable],
        saved_defaults: Optional[Dict[str, str]] = None,
        cli_title: Optional[str] = None
) -> ArgumentParser:
    """
    Dynamically creates a CLI from with a command for each operation.
    Help info for each operation and its arguments be retrieved from the function doc string
    operations: List of functions to create a CLI command for.
    saved_defaults: Values to use as default for the CLI commands. CLI params will be optional if its default is present
    cli_title: The title to given to the CLI
    """
    saved_defaults = saved_defaults or {}

    if not operations:
        raise ValueError('No operations given to generate CLI')

    parent_parser = _create_parent_parser(cli_title)
    sub_parsers = parent_parser.add_subparsers(dest='operation', required=True)

    for function in operations:
        # Attempt to retrieve help info from the doc string
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
                help=operation_help.arguments_help.get(param.name),
                required=not snake_case_to_camel_case(param.name) in saved_defaults,
                default=saved_defaults.get(snake_case_to_camel_case(param.name))
            )

    return parent_parser


def _create_parent_parser(cli_title: Optional[str]) -> ArgumentParser:
    parser = ArgumentParser(description=cli_title)
    parser.add_argument(
        '-v', '--verbose', action='store_true', required=False,
        help='Includes INFO logs to operation execution'
    )
    return parser


def _get_arg_type(cls: type) -> Union[type, Callable[[str], BkBaseModel]]:
    if cls is str:
        return None
    elif cls in [int, float, bool]:
        return cls
    return partial(_resolve_object_from_dict_str, cls)


def _resolve_object_from_dict_str(cls: Type[BkBaseModel], data: str) -> BkBaseModel:
    return cls.parse_raw(data)
