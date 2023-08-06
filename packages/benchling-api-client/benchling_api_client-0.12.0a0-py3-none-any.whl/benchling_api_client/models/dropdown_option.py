from typing import Any, Dict, Union

import attr

from ..models.dropdown_option_archive_record import DropdownOptionArchiveRecord
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class DropdownOption:
    """  """

    id: str
    name: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, DropdownOptionArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DropdownOption":
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = DropdownOptionArchiveRecord.from_dict(_archive_record)

        dropdown_option = DropdownOption(
            id=id,
            name=name,
            archive_record=archive_record,
        )

        return dropdown_option
