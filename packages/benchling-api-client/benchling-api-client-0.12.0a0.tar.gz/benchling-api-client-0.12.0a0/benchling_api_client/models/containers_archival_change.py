from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class ContainersArchivalChange:
    """IDs of all items that were unarchived, grouped by resource type. This includes the IDs of containers that were unarchived."""

    container_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerIds": container_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ContainersArchivalChange":
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds"))

        containers_archival_change = ContainersArchivalChange(
            container_ids=container_ids,
        )

        return containers_archival_change
