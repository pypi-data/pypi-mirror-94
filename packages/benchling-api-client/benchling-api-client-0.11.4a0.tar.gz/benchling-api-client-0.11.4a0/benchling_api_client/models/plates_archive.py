from typing import Any, Dict, List, cast

import attr

from ..models.plates_archive_reason import PlatesArchiveReason


@attr.s(auto_attribs=True)
class PlatesArchive:
    """  """

    plate_ids: List[str]
    reason: PlatesArchiveReason
    should_remove_barcodes: bool

    def to_dict(self) -> Dict[str, Any]:
        plate_ids = self.plate_ids

        reason = self.reason.value

        should_remove_barcodes = self.should_remove_barcodes

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "plateIds": plate_ids,
                "reason": reason,
                "shouldRemoveBarcodes": should_remove_barcodes,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "PlatesArchive":
        d = src_dict.copy()
        plate_ids = cast(List[str], d.pop("plateIds"))

        reason = PlatesArchiveReason(d.pop("reason"))

        should_remove_barcodes = d.pop("shouldRemoveBarcodes")

        plates_archive = PlatesArchive(
            plate_ids=plate_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )

        return plates_archive
