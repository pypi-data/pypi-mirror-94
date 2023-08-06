from typing import Any, Dict

import attr

from ..models.entry import Entry


@attr.s(auto_attribs=True)
class EntryById:
    """  """

    entry: Entry

    def to_dict(self) -> Dict[str, Any]:
        entry = self.entry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entry": entry,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntryById":
        d = src_dict.copy()
        entry = Entry.from_dict(d.pop("entry"))

        entry_by_id = EntryById(
            entry=entry,
        )

        return entry_by_id
