from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.tag_schema import TagSchema

T = TypeVar("T", bound="TagSchemasPaginatedList")


@attr.s(auto_attribs=True)
class TagSchemasPaginatedList:
    """  """

    next_token: str
    entity_schemas: List[TagSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        entity_schemas = []
        for entity_schemas_item_data in self.entity_schemas:
            entity_schemas_item = entity_schemas_item_data.to_dict()

            entity_schemas.append(entity_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "entitySchemas": entity_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        entity_schemas = []
        _entity_schemas = d.pop("entitySchemas")
        for entity_schemas_item_data in _entity_schemas:
            entity_schemas_item = TagSchema.from_dict(entity_schemas_item_data)

            entity_schemas.append(entity_schemas_item)

        tag_schemas_paginated_list = cls(
            next_token=next_token,
            entity_schemas=entity_schemas,
        )

        return tag_schemas_paginated_list
