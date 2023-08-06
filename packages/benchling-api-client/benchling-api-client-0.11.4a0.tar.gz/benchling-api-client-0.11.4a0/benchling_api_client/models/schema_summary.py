from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class SchemaSummary:
    """  """

    id: str
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SchemaSummary":
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        schema_summary = SchemaSummary(
            id=id,
            name=name,
        )

        return schema_summary
