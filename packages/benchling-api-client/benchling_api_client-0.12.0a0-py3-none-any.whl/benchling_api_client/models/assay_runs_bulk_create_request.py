from typing import Any, Dict, List

import attr

from ..models.assay_run_create import AssayRunCreate


@attr.s(auto_attribs=True)
class AssayRunsBulkCreateRequest:
    """  """

    assay_runs: List[AssayRunCreate]

    def to_dict(self) -> Dict[str, Any]:
        assay_runs = []
        for assay_runs_item_data in self.assay_runs:
            assay_runs_item = assay_runs_item_data.to_dict()

            assay_runs.append(assay_runs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayRuns": assay_runs,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayRunsBulkCreateRequest":
        d = src_dict.copy()
        assay_runs = []
        _assay_runs = d.pop("assayRuns")
        for assay_runs_item_data in _assay_runs:
            assay_runs_item = AssayRunCreate.from_dict(assay_runs_item_data)

            assay_runs.append(assay_runs_item)

        assay_runs_bulk_create_request = AssayRunsBulkCreateRequest(
            assay_runs=assay_runs,
        )

        return assay_runs_bulk_create_request
