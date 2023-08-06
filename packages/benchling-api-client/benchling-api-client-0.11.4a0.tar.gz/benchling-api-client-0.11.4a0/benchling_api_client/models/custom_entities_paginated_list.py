from typing import Any, Dict, List

import attr

from ..models.custom_entity import CustomEntity


@attr.s(auto_attribs=True)
class CustomEntitiesPaginatedList:
    """  """

    custom_entities: List[CustomEntity]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        custom_entities = []
        for custom_entities_item_data in self.custom_entities:
            custom_entities_item = custom_entities_item_data.to_dict()

            custom_entities.append(custom_entities_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "customEntities": custom_entities,
                "nextToken": next_token,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "CustomEntitiesPaginatedList":
        d = src_dict.copy()
        custom_entities = []
        _custom_entities = d.pop("customEntities")
        for custom_entities_item_data in _custom_entities:
            custom_entities_item = CustomEntity.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        next_token = d.pop("nextToken")

        custom_entities_paginated_list = CustomEntitiesPaginatedList(
            custom_entities=custom_entities,
            next_token=next_token,
        )

        return custom_entities_paginated_list
