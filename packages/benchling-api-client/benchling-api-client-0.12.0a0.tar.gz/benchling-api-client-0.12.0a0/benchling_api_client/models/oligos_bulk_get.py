from typing import Any, Dict, List

import attr

from ..models.oligo import Oligo


@attr.s(auto_attribs=True)
class OligosBulkGet:
    """  """

    oligos: List[Oligo]

    def to_dict(self) -> Dict[str, Any]:
        oligos = []
        for oligos_item_data in self.oligos:
            oligos_item = oligos_item_data.to_dict()

            oligos.append(oligos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "oligos": oligos,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "OligosBulkGet":
        d = src_dict.copy()
        oligos = []
        _oligos = d.pop("oligos")
        for oligos_item_data in _oligos:
            oligos_item = Oligo.from_dict(oligos_item_data)

            oligos.append(oligos_item)

        oligos_bulk_get = OligosBulkGet(
            oligos=oligos,
        )

        return oligos_bulk_get
