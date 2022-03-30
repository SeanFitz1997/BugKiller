import arrow

from bug_killer_app.datastore.project_table.project_item import ProjectItem, ProjectAssociationPrefix
from bug_killer_app.models.bug_resolution import BkAppBugResolution
from bug_killer_api_interface.schemas.entities.bug import Bug
from bug_killer_utils.strings import remove_prefix


class BkAppBug(Bug):
    _BUG_RESOLUTION_CLS = BkAppBugResolution

    @classmethod
    def from_db_item(cls: type, db_item: ProjectItem) -> 'BkAppBug':
        bug_id = remove_prefix(ProjectAssociationPrefix.BUG.value, db_item.project_association)
        bug_resolution = BkAppBugResolution.from_db_attribute(db_item.bug_resolution) \
            if db_item.bug_resolution else None

        return cls(
            id=bug_id,
            title=db_item.title,
            description=db_item.description,
            tags=list(db_item.tags),
            created_on=arrow.get(db_item.created_on),
            last_updated_on=arrow.get(db_item.last_updated_on),
            resolved=bug_resolution,
        )

    def to_db_item(self, project_id: str) -> ProjectItem:
        if self.resolved:
            if isinstance(self.resolved, BkAppBugResolution):
                resolved = self.resolved.to_db_attribute()
            else:
                raise ValueError(f'resolved must be a BkAppBugResolution but got {type(self.resolved).__name__}')
        else:
            resolved = None

        return ProjectItem(
            project_id=project_id,
            project_association=ProjectAssociationPrefix.BUG.value + self.id,
            title=self.title,
            description=self.description,
            created_on=self.created_on,
            last_updated_on=self.last_updated_on,
            tags=self.tags,
            bug_resolution=resolved
        )
