from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class PlatesUnarchive:
    """  """

    plate_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        plate_ids = self.plate_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "plateIds": plate_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "PlatesUnarchive":
        d = src_dict.copy()
        plate_ids = cast(List[str], d.pop("plateIds"))

        plates_unarchive = PlatesUnarchive(
            plate_ids=plate_ids,
        )

        return plates_unarchive
