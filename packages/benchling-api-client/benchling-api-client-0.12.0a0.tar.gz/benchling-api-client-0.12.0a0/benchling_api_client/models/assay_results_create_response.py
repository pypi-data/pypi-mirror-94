from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class AssayResultsCreateResponse:
    """  """

    assay_results: List[str]

    def to_dict(self) -> Dict[str, Any]:
        assay_results = self.assay_results

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResults": assay_results,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayResultsCreateResponse":
        d = src_dict.copy()
        assay_results = cast(List[str], d.pop("assayResults"))

        assay_results_create_response = AssayResultsCreateResponse(
            assay_results=assay_results,
        )

        return assay_results_create_response
