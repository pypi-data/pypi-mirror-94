from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class UnregisterEntities:
    """  """

    entity_ids: List[str]
    folder_id: str

    def to_dict(self) -> Dict[str, Any]:
        entity_ids = self.entity_ids

        folder_id = self.folder_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entityIds": entity_ids,
                "folderId": folder_id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "UnregisterEntities":
        d = src_dict.copy()
        entity_ids = cast(List[str], d.pop("entityIds"))

        folder_id = d.pop("folderId")

        unregister_entities = UnregisterEntities(
            entity_ids=entity_ids,
            folder_id=folder_id,
        )

        return unregister_entities
