from typing import Any, Dict

import attr

from ..models.entry_external_file import EntryExternalFile


@attr.s(auto_attribs=True)
class EntryExternalFileById:
    """  """

    external_file: EntryExternalFile

    def to_dict(self) -> Dict[str, Any]:
        external_file = self.external_file.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "externalFile": external_file,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntryExternalFileById":
        d = src_dict.copy()
        external_file = EntryExternalFile.from_dict(d.pop("externalFile"))

        entry_external_file_by_id = EntryExternalFileById(
            external_file=external_file,
        )

        return entry_external_file_by_id
