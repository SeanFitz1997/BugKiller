from typing import List, Optional, Tuple, TypeVar

from bug_killer.datastore.project_table.project_item import ProjectItem


T = TypeVar('T')

AllProjectItems = Tuple[ProjectItem, ProjectItem, List[ProjectItem], List[ProjectItem]]

OptionalProjectItems = Tuple[
    Optional[ProjectItem],
    Optional[ProjectItem],
    Optional[List[ProjectItem]],
    Optional[List[ProjectItem]],
]
