from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class DnaTemplateAlignmentFile:
    """  """

    name: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DnaTemplateAlignmentFile":
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        data = d.pop("data", UNSET)

        dna_template_alignment_file = DnaTemplateAlignmentFile(
            name=name,
            data=data,
        )

        return dna_template_alignment_file
