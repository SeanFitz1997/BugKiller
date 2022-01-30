from bug_killer_app.api.bug import get_bug_handler, create_bug_handler, update_bug_handler, resolve_bug_handler, \
    delete_bug_handler
from bug_killer_app.api.project import get_user_projects_handler, get_project_handler, create_project_handler, \
    update_project_handler, delete_project_handler


# This is needed so PyCharm will not mark these imports as unused
_ = get_user_projects_handler, get_project_handler, create_project_handler, update_project_handler, \
    delete_project_handler
_ = get_bug_handler, create_bug_handler, update_bug_handler, resolve_bug_handler, delete_bug_handler
