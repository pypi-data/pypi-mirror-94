from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class FoldersUnarchive:
    """  """

    folder_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        folder_ids = self.folder_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "folderIds": folder_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "FoldersUnarchive":
        d = src_dict.copy()
        folder_ids = cast(List[str], d.pop("folderIds"))

        folders_unarchive = FoldersUnarchive(
            folder_ids=folder_ids,
        )

        return folders_unarchive
