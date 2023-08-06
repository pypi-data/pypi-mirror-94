from typing import Any, Dict, List, cast

import attr

from ..models.oligos_archive_reason import OligosArchiveReason


@attr.s(auto_attribs=True)
class OligosArchive:
    """The request body for archiving Oligos."""

    reason: OligosArchiveReason
    oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        oligo_ids = self.oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "oligoIds": oligo_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "OligosArchive":
        d = src_dict.copy()
        reason = OligosArchiveReason(d.pop("reason"))

        oligo_ids = cast(List[str], d.pop("oligoIds"))

        oligos_archive = OligosArchive(
            reason=reason,
            oligo_ids=oligo_ids,
        )

        return oligos_archive
