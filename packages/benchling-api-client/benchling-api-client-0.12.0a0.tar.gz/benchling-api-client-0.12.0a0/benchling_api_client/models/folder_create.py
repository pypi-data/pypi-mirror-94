from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class FolderCreate:
    """  """

    name: str
    parent_folder_id: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        parent_folder_id = self.parent_folder_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "parentFolderId": parent_folder_id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "FolderCreate":
        d = src_dict.copy()
        name = d.pop("name")

        parent_folder_id = d.pop("parentFolderId")

        folder_create = FolderCreate(
            name=name,
            parent_folder_id=parent_folder_id,
        )

        return folder_create
