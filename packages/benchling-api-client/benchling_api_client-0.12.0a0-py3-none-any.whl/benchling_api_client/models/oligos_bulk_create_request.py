from typing import Any, Dict, List, Union

import attr

from ..models.oligo_bulk_create import OligoBulkCreate
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class OligosBulkCreateRequest:
    """  """

    oligos: Union[Unset, List[OligoBulkCreate]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        oligos: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.oligos, Unset):
            oligos = []
            for oligos_item_data in self.oligos:
                oligos_item = oligos_item_data.to_dict()

                oligos.append(oligos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if oligos is not UNSET:
            field_dict["oligos"] = oligos

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "OligosBulkCreateRequest":
        d = src_dict.copy()
        oligos = []
        _oligos = d.pop("oligos", UNSET)
        for oligos_item_data in _oligos or []:
            oligos_item = OligoBulkCreate.from_dict(oligos_item_data)

            oligos.append(oligos_item)

        oligos_bulk_create_request = OligosBulkCreateRequest(
            oligos=oligos,
        )

        return oligos_bulk_create_request
