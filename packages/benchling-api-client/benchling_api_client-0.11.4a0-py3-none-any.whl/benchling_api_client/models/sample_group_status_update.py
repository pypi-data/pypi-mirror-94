from typing import Any, Dict

import attr

from ..models.sample_group_status import SampleGroupStatus


@attr.s(auto_attribs=True)
class SampleGroupStatusUpdate:
    """  """

    sample_group_id: str
    status: SampleGroupStatus

    def to_dict(self) -> Dict[str, Any]:
        sample_group_id = self.sample_group_id
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sampleGroupId": sample_group_id,
                "status": status,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SampleGroupStatusUpdate":
        d = src_dict.copy()
        sample_group_id = d.pop("sampleGroupId")

        status = SampleGroupStatus(d.pop("status"))

        sample_group_status_update = SampleGroupStatusUpdate(
            sample_group_id=sample_group_id,
            status=status,
        )

        return sample_group_status_update
