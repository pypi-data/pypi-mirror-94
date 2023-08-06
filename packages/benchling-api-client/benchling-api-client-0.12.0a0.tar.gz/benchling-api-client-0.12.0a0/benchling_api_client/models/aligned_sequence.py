from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AlignedSequence:
    """  """

    bases: Union[Unset, str] = UNSET
    dna_sequence_id: Union[Unset, str] = UNSET
    trim_end: Union[Unset, int] = UNSET
    trim_start: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        bases = self.bases
        dna_sequence_id = self.dna_sequence_id
        trim_end = self.trim_end
        trim_start = self.trim_start
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if bases is not UNSET:
            field_dict["bases"] = bases
        if dna_sequence_id is not UNSET:
            field_dict["dnaSequenceId"] = dna_sequence_id
        if trim_end is not UNSET:
            field_dict["trimEnd"] = trim_end
        if trim_start is not UNSET:
            field_dict["trimStart"] = trim_start
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AlignedSequence":
        d = src_dict.copy()
        bases = d.pop("bases", UNSET)

        dna_sequence_id = d.pop("dnaSequenceId", UNSET)

        trim_end = d.pop("trimEnd", UNSET)

        trim_start = d.pop("trimStart", UNSET)

        name = d.pop("name", UNSET)

        aligned_sequence = AlignedSequence(
            bases=bases,
            dna_sequence_id=dna_sequence_id,
            trim_end=trim_end,
            trim_start=trim_start,
            name=name,
        )

        return aligned_sequence
