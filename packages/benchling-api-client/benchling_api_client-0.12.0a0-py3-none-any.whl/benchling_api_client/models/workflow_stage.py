import datetime
from typing import Any, Dict

import attr
from dateutil.parser import isoparse


@attr.s(auto_attribs=True)
class WorkflowStage:
    """  """

    id: str
    name: str
    created_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "createdAt": created_at,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "WorkflowStage":
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))

        workflow_stage = WorkflowStage(
            id=id,
            name=name,
            created_at=created_at,
        )

        return workflow_stage
