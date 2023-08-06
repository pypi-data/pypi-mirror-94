from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class ArchiveRecord:
    """  """

    reason: str

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ArchiveRecord":
        d = src_dict.copy()
        reason = d.pop("reason")

        archive_record = ArchiveRecord(
            reason=reason,
        )

        return archive_record
