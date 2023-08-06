from typing import Any, Dict, List

import attr

from ..models.batch_entity_schema import BatchEntitySchema


@attr.s(auto_attribs=True)
class BatchSchemasList:
    """  """

    batch_schemas: List[BatchEntitySchema]

    def to_dict(self) -> Dict[str, Any]:
        batch_schemas = []
        for batch_schemas_item_data in self.batch_schemas:
            batch_schemas_item = batch_schemas_item_data.to_dict()

            batch_schemas.append(batch_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batchSchemas": batch_schemas,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BatchSchemasList":
        d = src_dict.copy()
        batch_schemas = []
        _batch_schemas = d.pop("batchSchemas")
        for batch_schemas_item_data in _batch_schemas:
            batch_schemas_item = BatchEntitySchema.from_dict(batch_schemas_item_data)

            batch_schemas.append(batch_schemas_item)

        batch_schemas_list = BatchSchemasList(
            batch_schemas=batch_schemas,
        )

        return batch_schemas_list
