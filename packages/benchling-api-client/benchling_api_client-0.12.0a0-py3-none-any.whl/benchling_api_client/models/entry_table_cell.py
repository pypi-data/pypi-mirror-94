from typing import Any, Dict, Union

import attr

from ..models.entry_link import EntryLink
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class EntryTableCell:
    """  """

    text: Union[Unset, str] = UNSET
    link: Union[Unset, EntryLink] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        link: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.link, Unset):
            link = self.link.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if text is not UNSET:
            field_dict["text"] = text
        if link is not UNSET:
            field_dict["link"] = link

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntryTableCell":
        d = src_dict.copy()
        text = d.pop("text", UNSET)

        link: Union[Unset, EntryLink] = UNSET
        _link = d.pop("link", UNSET)
        if not isinstance(_link, Unset):
            link = EntryLink.from_dict(_link)

        entry_table_cell = EntryTableCell(
            text=text,
            link=link,
        )

        return entry_table_cell
