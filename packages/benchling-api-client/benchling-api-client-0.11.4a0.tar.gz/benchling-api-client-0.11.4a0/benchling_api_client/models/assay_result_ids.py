from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class AssayResultIds:
    """  """

    assay_result_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        assay_result_ids = self.assay_result_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResultIds": assay_result_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayResultIds":
        d = src_dict.copy()
        assay_result_ids = cast(List[str], d.pop("assayResultIds"))

        assay_result_ids = AssayResultIds(
            assay_result_ids=assay_result_ids,
        )

        return assay_result_ids
