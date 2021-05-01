import logging
from typing import List

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, UnicodeSetAttribute
from pynamodb.models import Model

from bug_killer.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute


class ProjectItem(Model):
    class Meta:
        table_name = 'ProjectTable'
        region = 'eu-west-1'


    PROJECT_SK_PREFIX = 'P'
    BUG_SK_PREFIX = 'B'

    # Table Keys
    project_id = UnicodeAttribute(hash_key=True)
    project_bug_user_id = UnicodeAttribute(range_key=True)

    # Project Attributes
    project_manager_id = UnicodeAttribute(null=True)

    # Bug Attributes
    bug_resolution = BugResolutionMapAttribute(null=True)

    # Common Attributes
    title = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)
    created_on = UTCDateTimeAttribute(null=True)
    last_updated_on = UTCDateTimeAttribute(null=True)
    tags = UnicodeSetAttribute(null=True)


def get_project_item_by_id(project_id: str) -> ProjectItem:
    sort_key = ProjectItem.PROJECT_SK_PREFIX + project_id
    logging.info(f'Getting project db item by HK: {project_id}, SK: {sort_key}')
    project_db_item = ProjectItem.get(project_id, sort_key)
    logging.info(f'Got project db item {project_db_item}')
    return project_db_item


def get_bug_items_by_project_id(project_id: str) -> List[ProjectItem]:
    sort_key = ProjectItem.project_bug_user_id.startswith(ProjectItem.BUG_SK_PREFIX)
    logging.info(f'Getting bug db items by HK: {project_id}, SK: {sort_key}')
    bug_db_items = ProjectItem.query(project_id, sort_key)
    logging.info(f'Got bug items {bug_db_items}')
    return bug_db_items
