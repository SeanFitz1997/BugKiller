import asyncio
import logging
from argparse import Namespace
from inspect import signature
from typing import List, Callable, Any

from bug_killer_utils.strings import camel_case_to_snake_case, snake_case_to_camel_case


def execute_operation(operations: List[Callable], cli_args: Namespace) -> Any:
    """
    Executes the operation specified in the cli command with the data given as options.
    Will use the data in the saved defaults if the option is not given
    """
    # Set logging if enabled
    if cli_args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    # Get the specified operation
    operation_name = camel_case_to_snake_case(cli_args.operation)
    operation = next(operation for operation in operations if operation.__name__ == operation_name)

    # Extract the params needed for the function
    function_signature = signature(operation)
    operation_args = {
        param: getattr(cli_args, snake_case_to_camel_case(param)) for param in function_signature.parameters
    }

    # Execute the operation
    return asyncio.run(operation(**operation_args))
