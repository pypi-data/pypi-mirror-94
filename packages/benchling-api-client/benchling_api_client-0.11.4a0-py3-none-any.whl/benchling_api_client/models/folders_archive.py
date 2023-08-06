from typing import Any, Dict, List, cast

import attr

from ..models.folders_archive_reason import FoldersArchiveReason


@attr.s(auto_attribs=True)
class FoldersArchive:
    """  """

    reason: FoldersArchiveReason
    folder_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        folder_ids = self.folder_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "folderIds": folder_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "FoldersArchive":
        d = src_dict.copy()
        reason = FoldersArchiveReason(d.pop("reason"))

        folder_ids = cast(List[str], d.pop("folderIds"))

        folders_archive = FoldersArchive(
            reason=reason,
            folder_ids=folder_ids,
        )

        return folders_archive
