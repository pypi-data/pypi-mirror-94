from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class EntriesUnarchive:
    """  """

    entry_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        entry_ids = self.entry_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entryIds": entry_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntriesUnarchive":
        d = src_dict.copy()
        entry_ids = cast(List[str], d.pop("entryIds"))

        entries_unarchive = EntriesUnarchive(
            entry_ids=entry_ids,
        )

        return entries_unarchive
