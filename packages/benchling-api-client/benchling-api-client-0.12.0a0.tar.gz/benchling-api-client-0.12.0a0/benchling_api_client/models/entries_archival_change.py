from typing import Any, Dict, List, Union, cast

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class EntriesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of entries that changed.."""

    entry_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entry_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.entry_ids, Unset):
            entry_ids = self.entry_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entry_ids is not UNSET:
            field_dict["entryIds"] = entry_ids

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntriesArchivalChange":
        d = src_dict.copy()
        entry_ids = cast(List[str], d.pop("entryIds", UNSET))

        entries_archival_change = EntriesArchivalChange(
            entry_ids=entry_ids,
        )

        return entries_archival_change
