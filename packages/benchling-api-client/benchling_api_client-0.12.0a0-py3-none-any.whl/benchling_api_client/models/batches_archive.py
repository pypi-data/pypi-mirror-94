from typing import Any, Dict, List, cast

import attr

from ..models.batches_archive_reason import BatchesArchiveReason


@attr.s(auto_attribs=True)
class BatchesArchive:
    """The request body for archiving Batches."""

    reason: BatchesArchiveReason
    batch_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        batch_ids = self.batch_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "batchIds": batch_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BatchesArchive":
        d = src_dict.copy()
        reason = BatchesArchiveReason(d.pop("reason"))

        batch_ids = cast(List[str], d.pop("batchIds"))

        batches_archive = BatchesArchive(
            reason=reason,
            batch_ids=batch_ids,
        )

        return batches_archive
