from typing import Any, Dict, List, Union, cast

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AssayRunsBulkCreateResponse:
    """  """

    assay_runs: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        assay_runs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.assay_runs, Unset):
            assay_runs = self.assay_runs

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if assay_runs is not UNSET:
            field_dict["assayRuns"] = assay_runs

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayRunsBulkCreateResponse":
        d = src_dict.copy()
        assay_runs = cast(List[str], d.pop("assayRuns", UNSET))

        assay_runs_bulk_create_response = AssayRunsBulkCreateResponse(
            assay_runs=assay_runs,
        )

        return assay_runs_bulk_create_response
