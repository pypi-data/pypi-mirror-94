from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class DropdownOptionUpdate:
    """  """

    name: str
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DropdownOptionUpdate":
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        dropdown_option_update = DropdownOptionUpdate(
            name=name,
            id=id,
        )

        return dropdown_option_update
