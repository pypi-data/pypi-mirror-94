from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class SampleGroups:
    """ Array of SampleGroup resources """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SampleGroups":
        src_dict.copy()
        sample_groups = SampleGroups()

        return sample_groups
