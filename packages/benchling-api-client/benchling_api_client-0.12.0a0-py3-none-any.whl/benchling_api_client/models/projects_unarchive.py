from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class ProjectsUnarchive:
    """  """

    project_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        project_ids = self.project_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectIds": project_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ProjectsUnarchive":
        d = src_dict.copy()
        project_ids = cast(List[str], d.pop("projectIds"))

        projects_unarchive = ProjectsUnarchive(
            project_ids=project_ids,
        )

        return projects_unarchive
