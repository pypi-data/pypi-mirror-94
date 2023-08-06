from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class TeamSummary:
    """  """

    id: str
    name: Union[Unset, str] = UNSET
    handle: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        handle = self.handle

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if handle is not UNSET:
            field_dict["handle"] = handle

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "TeamSummary":
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        handle = d.pop("handle", UNSET)

        team_summary = TeamSummary(
            id=id,
            name=name,
            handle=handle,
        )

        return team_summary
