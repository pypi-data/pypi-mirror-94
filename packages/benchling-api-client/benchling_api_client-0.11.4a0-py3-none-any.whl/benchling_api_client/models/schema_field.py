from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class SchemaField:
    """  """

    is_required: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        is_required = self.is_required
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SchemaField":
        d = src_dict.copy()
        is_required = d.pop("isRequired", UNSET)

        name = d.pop("name", UNSET)

        schema_field = SchemaField(
            is_required=is_required,
            name=name,
        )

        return schema_field
