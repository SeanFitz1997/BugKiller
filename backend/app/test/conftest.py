from subprocess import Popen

import pytest

from test.helpers import wait_for_port_to_open
from test.test_doubles.db.db_setup import delete_project_table, setup_project_table


DDB_PORT = 8000


def run_local_ddb(port):
    local_ddb_process = None
    try:
        local_ddb_process = Popen(f"dynalite --port {port}", shell=True)
        yield
    finally:
        if local_ddb_process:
            local_ddb_process.kill()
            local_ddb_process.wait()


@pytest.fixture(scope="session", autouse=True)
def local_ddb():
    local_ddb_process = None
    try:
        local_ddb_process = Popen(f"dynalite --port {DDB_PORT}", shell=True)
        wait_for_port_to_open(DDB_PORT)
        yield
    finally:
        if local_ddb_process:
            local_ddb_process.kill()
            local_ddb_process.wait()


@pytest.fixture(scope="session", autouse=True)
def project_table(local_ddb):
    setup_project_table(DDB_PORT)
    yield
    delete_project_table()
