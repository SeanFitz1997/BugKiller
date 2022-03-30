from typing import NoReturn

from bug_killer_client_2.cli.builder import generate_cli
from bug_killer_client_2.cli.builder import get_cli_defaults
from bug_killer_client_2.cli.executor import execute_operation
from bug_killer_client_2.service import project, bug
from bug_killer_utils.object import get_local_function_in_module


def main() -> NoReturn:
    defaults = get_cli_defaults()
    operations = get_local_function_in_module(project) + get_local_function_in_module(bug)
    parser = generate_cli(operations, defaults, 'BugKiller CLI')
    execute_operation(operations, parser.parse_args())


if __name__ == '__main__':
    main()
