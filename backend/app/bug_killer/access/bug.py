import logging
from typing import List

from bug_killer.datastore.project_item import get_bug_items_by_project_id
from bug_killer.models.bug import Bug


def get_bugs_by_project_id(project_id: str) -> List[Bug]:
    logging.info(f'Getting bugs for project {project_id}')
    bug_db_items = get_bug_items_by_project_id(project_id)
    return [Bug.from_db_item(item) for item in bug_db_items]
