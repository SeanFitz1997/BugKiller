from typing import NoReturn

from bug_killer_app.util.entity import get_local_function_in_module
from bug_killer_client.cli.builder import generate_cli
from bug_killer_client.cli.executor import execute_operation
from bug_killer_client.cli.util import get_cli_defaults
from bug_killer_client.service import project, bug


def main() -> NoReturn:
    defaults = get_cli_defaults()
    operations = get_local_function_in_module(project) + get_local_function_in_module(bug)
    parser = generate_cli(operations, defaults, 'BugKiller CLI')
    execute_operation(operations, parser.parse_args(), defaults)


if __name__ == '__main__':
    main()
