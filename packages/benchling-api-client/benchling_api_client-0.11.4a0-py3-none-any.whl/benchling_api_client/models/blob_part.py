from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class BlobPart:
    """  """

    part_number: Union[Unset, int] = UNSET
    e_tag: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        part_number = self.part_number
        e_tag = self.e_tag

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if e_tag is not UNSET:
            field_dict["eTag"] = e_tag

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BlobPart":
        d = src_dict.copy()
        part_number = d.pop("partNumber", UNSET)

        e_tag = d.pop("eTag", UNSET)

        blob_part = BlobPart(
            part_number=part_number,
            e_tag=e_tag,
        )

        return blob_part
