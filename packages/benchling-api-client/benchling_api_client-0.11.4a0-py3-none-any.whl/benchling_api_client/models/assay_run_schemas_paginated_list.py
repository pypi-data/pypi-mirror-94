from typing import Any, Dict, List

import attr

from ..models.assay_run_schema import AssayRunSchema


@attr.s(auto_attribs=True)
class AssayRunSchemasPaginatedList:
    """  """

    assay_run_schemas: List[AssayRunSchema]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        assay_run_schemas = []
        for assay_run_schemas_item_data in self.assay_run_schemas:
            assay_run_schemas_item = assay_run_schemas_item_data.to_dict()

            assay_run_schemas.append(assay_run_schemas_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayRunSchemas": assay_run_schemas,
                "nextToken": next_token,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayRunSchemasPaginatedList":
        d = src_dict.copy()
        assay_run_schemas = []
        _assay_run_schemas = d.pop("assayRunSchemas")
        for assay_run_schemas_item_data in _assay_run_schemas:
            assay_run_schemas_item = AssayRunSchema.from_dict(assay_run_schemas_item_data)

            assay_run_schemas.append(assay_run_schemas_item)

        next_token = d.pop("nextToken")

        assay_run_schemas_paginated_list = AssayRunSchemasPaginatedList(
            assay_run_schemas=assay_run_schemas,
            next_token=next_token,
        )

        return assay_run_schemas_paginated_list
