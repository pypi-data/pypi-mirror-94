from typing import Any, Dict, List

import attr

from ..models.dropdown_summary import DropdownSummary


@attr.s(auto_attribs=True)
class DropdownsRegistryList:
    """  """

    dropdowns: List[DropdownSummary]

    def to_dict(self) -> Dict[str, Any]:
        dropdowns = []
        for dropdowns_item_data in self.dropdowns:
            dropdowns_item = dropdowns_item_data.to_dict()

            dropdowns.append(dropdowns_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dropdowns": dropdowns,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DropdownsRegistryList":
        d = src_dict.copy()
        dropdowns = []
        _dropdowns = d.pop("dropdowns")
        for dropdowns_item_data in _dropdowns:
            dropdowns_item = DropdownSummary.from_dict(dropdowns_item_data)

            dropdowns.append(dropdowns_item)

        dropdowns_registry_list = DropdownsRegistryList(
            dropdowns=dropdowns,
        )

        return dropdowns_registry_list
