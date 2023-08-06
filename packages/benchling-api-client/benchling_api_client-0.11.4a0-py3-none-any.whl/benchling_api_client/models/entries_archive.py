from typing import Any, Dict, List, cast

import attr

from ..models.entries_archive_reason import EntriesArchiveReason


@attr.s(auto_attribs=True)
class EntriesArchive:
    """  """

    entry_ids: List[str]
    reason: EntriesArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        entry_ids = self.entry_ids

        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entryIds": entry_ids,
                "reason": reason,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntriesArchive":
        d = src_dict.copy()
        entry_ids = cast(List[str], d.pop("entryIds"))

        reason = EntriesArchiveReason(d.pop("reason"))

        entries_archive = EntriesArchive(
            entry_ids=entry_ids,
            reason=reason,
        )

        return entries_archive
