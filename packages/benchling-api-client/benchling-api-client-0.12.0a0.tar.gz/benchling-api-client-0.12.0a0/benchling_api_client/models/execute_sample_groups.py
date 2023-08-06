from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class ExecuteSampleGroups:
    """The response is intentionally empty."""

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ExecuteSampleGroups":
        src_dict.copy()
        execute_sample_groups = ExecuteSampleGroups()

        return execute_sample_groups
