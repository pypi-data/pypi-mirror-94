from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class DnaSequencesUnarchive:
    """The request body for unarchiving DNA sequences."""

    dna_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids = self.dna_sequence_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaSequenceIds": dna_sequence_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DnaSequencesUnarchive":
        d = src_dict.copy()
        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds"))

        dna_sequences_unarchive = DnaSequencesUnarchive(
            dna_sequence_ids=dna_sequence_ids,
        )

        return dna_sequences_unarchive
