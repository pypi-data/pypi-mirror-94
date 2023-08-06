from typing import Any, Dict, List, Union, cast

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class BatchesArchivalChange:
    """IDs of all batches that were archived / unarchived, grouped by resource type."""

    batch_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.batch_ids, Unset):
            batch_ids = self.batch_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BatchesArchivalChange":
        d = src_dict.copy()
        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        batches_archival_change = BatchesArchivalChange(
            batch_ids=batch_ids,
        )

        return batches_archival_change
