from typing import Any, Dict, List

import attr

from ..models.tag_schema import TagSchema


@attr.s(auto_attribs=True)
class TagSchemasList:
    """  """

    entity_schemas: List[TagSchema]

    def to_dict(self) -> Dict[str, Any]:
        entity_schemas = []
        for entity_schemas_item_data in self.entity_schemas:
            entity_schemas_item = entity_schemas_item_data.to_dict()

            entity_schemas.append(entity_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entitySchemas": entity_schemas,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "TagSchemasList":
        d = src_dict.copy()
        entity_schemas = []
        _entity_schemas = d.pop("entitySchemas")
        for entity_schemas_item_data in _entity_schemas:
            entity_schemas_item = TagSchema.from_dict(entity_schemas_item_data)

            entity_schemas.append(entity_schemas_item)

        tag_schemas_list = TagSchemasList(
            entity_schemas=entity_schemas,
        )

        return tag_schemas_list
