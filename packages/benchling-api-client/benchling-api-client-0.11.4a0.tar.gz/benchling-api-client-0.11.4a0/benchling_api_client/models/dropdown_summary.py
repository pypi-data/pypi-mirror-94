from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class DropdownSummary:
    """  """

    name: str
    id: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "id": id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DropdownSummary":
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id")

        dropdown_summary = DropdownSummary(
            name=name,
            id=id,
        )

        return dropdown_summary
