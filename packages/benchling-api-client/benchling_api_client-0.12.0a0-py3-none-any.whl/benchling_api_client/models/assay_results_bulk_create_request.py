from typing import Any, Dict, List

import attr

from ..models.assay_result_create import AssayResultCreate


@attr.s(auto_attribs=True)
class AssayResultsBulkCreateRequest:
    """  """

    assay_results: List[AssayResultCreate]

    def to_dict(self) -> Dict[str, Any]:
        assay_results = []
        for assay_results_item_data in self.assay_results:
            assay_results_item = assay_results_item_data.to_dict()

            assay_results.append(assay_results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResults": assay_results,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayResultsBulkCreateRequest":
        d = src_dict.copy()
        assay_results = []
        _assay_results = d.pop("assayResults")
        for assay_results_item_data in _assay_results:
            assay_results_item = AssayResultCreate.from_dict(assay_results_item_data)

            assay_results.append(assay_results_item)

        assay_results_bulk_create_request = AssayResultsBulkCreateRequest(
            assay_results=assay_results,
        )

        return assay_results_bulk_create_request
