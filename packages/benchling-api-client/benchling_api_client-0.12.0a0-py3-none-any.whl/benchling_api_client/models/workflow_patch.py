from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class WorkflowPatch:
    """  """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if project_id is not UNSET:
            field_dict["projectId"] = project_id

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "WorkflowPatch":
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        project_id = d.pop("projectId", UNSET)

        workflow_patch = WorkflowPatch(
            name=name,
            description=description,
            project_id=project_id,
        )

        return workflow_patch
