from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class OligosUnarchive:
    """The request body for unarchiving Oligos."""

    oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        oligo_ids = self.oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "oligoIds": oligo_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "OligosUnarchive":
        d = src_dict.copy()
        oligo_ids = cast(List[str], d.pop("oligoIds"))

        oligos_unarchive = OligosUnarchive(
            oligo_ids=oligo_ids,
        )

        return oligos_unarchive
