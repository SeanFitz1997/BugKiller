import asyncio
import json
import logging
from argparse import Namespace
from inspect import signature
from typing import NoReturn, List, Callable, Optional, Dict

from bug_killer_utils.strings import camel_case_to_snake_case, snake_case_to_camel_case


def execute_operation(
        operations: List[Callable],
        cli_args: Namespace,
        saved_defaults: Optional[Dict[str, str]] = None
) -> NoReturn:
    """
    Executes the operation specified in the cli command with the data given as options.
    Will use the data in the saved defaults if the option is not given
    """
    saved_defaults = saved_defaults or {}

    # Set logging if enabled
    logging.getLogger().setLevel(logging.INFO if cli_args.verbose else logging.ERROR)

    # Get the specified operation
    operation_name = camel_case_to_snake_case(cli_args.operation)
    operation = next(operation for operation in operations if operation.__name__ == operation_name)

    # Extract the params needed for the function
    function_signature = signature(operation)
    operation_args = {}

    for param in function_signature.parameters:
        param_snake_case = param
        param_camel_case = snake_case_to_camel_case(param)

        # Try to get the value from defaults
        if defaults_value := saved_defaults.get(param_camel_case):
            operation_args[param_snake_case] = defaults_value

        # Try to get the value from the CLI options
        if arg_value := getattr(cli_args, snake_case_to_camel_case(param), lambda: None):
            operation_args[param] = arg_value

    # Execute the operation
    rsp = asyncio.run(operation(**operation_args))

    # Print the response with colour
    rsp_json = json.dumps(rsp.to_dict(), indent=4)
    print(rsp_json)
