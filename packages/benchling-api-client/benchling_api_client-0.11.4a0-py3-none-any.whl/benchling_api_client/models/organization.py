from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Organization:
    """  """

    id: str
    handle: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        handle = self.handle
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if handle is not UNSET:
            field_dict["handle"] = handle
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Organization":
        d = src_dict.copy()
        id = d.pop("id")

        handle = d.pop("handle", UNSET)

        name = d.pop("name", UNSET)

        organization = Organization(
            id=id,
            handle=handle,
            name=name,
        )

        return organization
