from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class DropdownOptionCreate:
    """  """

    name: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DropdownOptionCreate":
        d = src_dict.copy()
        name = d.pop("name")

        dropdown_option_create = DropdownOptionCreate(
            name=name,
        )

        return dropdown_option_create
