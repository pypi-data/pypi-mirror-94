from typing import Any, Dict, Union

import attr

from ..models.organization import Organization
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Registry:
    """  """

    id: str
    name: Union[Unset, str] = UNSET
    owner: Union[Unset, Organization] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        owner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.owner, Unset):
            owner = self.owner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Registry":
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        owner: Union[Unset, Organization] = UNSET
        _owner = d.pop("owner", UNSET)
        if not isinstance(_owner, Unset):
            owner = Organization.from_dict(_owner)

        registry = Registry(
            id=id,
            name=name,
            owner=owner,
        )

        return registry
