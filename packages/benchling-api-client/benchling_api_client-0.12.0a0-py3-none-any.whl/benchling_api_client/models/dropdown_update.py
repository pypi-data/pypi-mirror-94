from typing import Any, Dict, List

import attr

from ..models.dropdown_option_update import DropdownOptionUpdate


@attr.s(auto_attribs=True)
class DropdownUpdate:
    """  """

    options: List[DropdownOptionUpdate]

    def to_dict(self) -> Dict[str, Any]:
        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()

            options.append(options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "options": options,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DropdownUpdate":
        d = src_dict.copy()
        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = DropdownOptionUpdate.from_dict(options_item_data)

            options.append(options_item)

        dropdown_update = DropdownUpdate(
            options=options,
        )

        return dropdown_update
