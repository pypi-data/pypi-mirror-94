from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class BoxesUnarchive:
    """  """

    box_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        box_ids = self.box_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "boxIds": box_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BoxesUnarchive":
        d = src_dict.copy()
        box_ids = cast(List[str], d.pop("boxIds"))

        boxes_unarchive = BoxesUnarchive(
            box_ids=box_ids,
        )

        return boxes_unarchive
