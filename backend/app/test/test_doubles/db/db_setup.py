from bug_killer.datastore.project_table.project_item import ProjectItem


def setup_project_table(db_port):
    ProjectItem.Meta.table_name = "ProjectTable"
    ProjectItem.Meta.host = f"http://localhost:{db_port}"

    # Credential values are not used, but must be given
    ProjectItem.Meta.aws_access_key_id = ""
    ProjectItem.Meta.aws_secret_access_key = ""
    ProjectItem.Meta.aws_session_token = ""

    ProjectItem.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


def delete_project_table():
    ProjectItem.delete_table()
