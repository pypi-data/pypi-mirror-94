from typing import Any, Dict, List

import attr

from ..models.sample_group_status_update import SampleGroupStatusUpdate


@attr.s(auto_attribs=True)
class SampleGroupsStatusUpdate:
    """ Specification to update status of sample groups on the request which were executed. """

    sample_groups: List[SampleGroupStatusUpdate]

    def to_dict(self) -> Dict[str, Any]:
        sample_groups = []
        for sample_groups_item_data in self.sample_groups:
            sample_groups_item = sample_groups_item_data.to_dict()

            sample_groups.append(sample_groups_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sampleGroups": sample_groups,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SampleGroupsStatusUpdate":
        d = src_dict.copy()
        sample_groups = []
        _sample_groups = d.pop("sampleGroups")
        for sample_groups_item_data in _sample_groups:
            sample_groups_item = SampleGroupStatusUpdate.from_dict(sample_groups_item_data)

            sample_groups.append(sample_groups_item)

        sample_groups_status_update = SampleGroupsStatusUpdate(
            sample_groups=sample_groups,
        )

        return sample_groups_status_update
