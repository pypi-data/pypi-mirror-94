from typing import Any, Dict, List

import attr

from ..models.folder import Folder


@attr.s(auto_attribs=True)
class FoldersPaginatedList:
    """  """

    next_token: str
    folders: List[Folder]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        folders = []
        for folders_item_data in self.folders:
            folders_item = folders_item_data.to_dict()

            folders.append(folders_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "folders": folders,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "FoldersPaginatedList":
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        folders = []
        _folders = d.pop("folders")
        for folders_item_data in _folders:
            folders_item = Folder.from_dict(folders_item_data)

            folders.append(folders_item)

        folders_paginated_list = FoldersPaginatedList(
            next_token=next_token,
            folders=folders,
        )

        return folders_paginated_list
