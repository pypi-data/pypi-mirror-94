from typing import Any, Dict, List

import attr

from ..models.assay_result import AssayResult


@attr.s(auto_attribs=True)
class AssayResultsBulkGet:
    """  """

    assay_results: List[AssayResult]

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
    def from_dict(src_dict: Dict[str, Any]) -> "AssayResultsBulkGet":
        d = src_dict.copy()
        assay_results = []
        _assay_results = d.pop("assayResults")
        for assay_results_item_data in _assay_results:
            assay_results_item = AssayResult.from_dict(assay_results_item_data)

            assay_results.append(assay_results_item)

        assay_results_bulk_get = AssayResultsBulkGet(
            assay_results=assay_results,
        )

        return assay_results_bulk_get
