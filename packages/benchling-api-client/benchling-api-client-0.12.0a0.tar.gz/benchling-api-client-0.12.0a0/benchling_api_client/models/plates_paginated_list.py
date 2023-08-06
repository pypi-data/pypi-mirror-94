from typing import Any, Dict, List

import attr

from ..models.plate import Plate


@attr.s(auto_attribs=True)
class PlatesPaginatedList:
    """  """

    next_token: str
    plates: List[Plate]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        plates = []
        for plates_item_data in self.plates:
            plates_item = plates_item_data.to_dict()

            plates.append(plates_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "plates": plates,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "PlatesPaginatedList":
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        plates = []
        _plates = d.pop("plates")
        for plates_item_data in _plates:
            plates_item = Plate.from_dict(plates_item_data)

            plates.append(plates_item)

        plates_paginated_list = PlatesPaginatedList(
            next_token=next_token,
            plates=plates,
        )

        return plates_paginated_list
