from typing import Any, Dict, List

import attr

from ..models.plate_schema import PlateSchema


@attr.s(auto_attribs=True)
class PlateSchemasList:
    """  """

    plate_schemas: List[PlateSchema]

    def to_dict(self) -> Dict[str, Any]:
        plate_schemas = []
        for plate_schemas_item_data in self.plate_schemas:
            plate_schemas_item = plate_schemas_item_data.to_dict()

            plate_schemas.append(plate_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "plateSchemas": plate_schemas,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "PlateSchemasList":
        d = src_dict.copy()
        plate_schemas = []
        _plate_schemas = d.pop("plateSchemas")
        for plate_schemas_item_data in _plate_schemas:
            plate_schemas_item = PlateSchema.from_dict(plate_schemas_item_data)

            plate_schemas.append(plate_schemas_item)

        plate_schemas_list = PlateSchemasList(
            plate_schemas=plate_schemas,
        )

        return plate_schemas_list
