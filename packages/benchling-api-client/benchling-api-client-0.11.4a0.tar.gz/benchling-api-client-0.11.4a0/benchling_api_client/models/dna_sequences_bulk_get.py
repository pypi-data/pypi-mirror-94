from typing import Any, Dict, List

import attr

from ..models.dna_sequence import DnaSequence


@attr.s(auto_attribs=True)
class DnaSequencesBulkGet:
    """  """

    dna_sequences: List[DnaSequence]

    def to_dict(self) -> Dict[str, Any]:
        dna_sequences = []
        for dna_sequences_item_data in self.dna_sequences:
            dna_sequences_item = dna_sequences_item_data.to_dict()

            dna_sequences.append(dna_sequences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaSequences": dna_sequences,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DnaSequencesBulkGet":
        d = src_dict.copy()
        dna_sequences = []
        _dna_sequences = d.pop("dnaSequences")
        for dna_sequences_item_data in _dna_sequences:
            dna_sequences_item = DnaSequence.from_dict(dna_sequences_item_data)

            dna_sequences.append(dna_sequences_item)

        dna_sequences_bulk_get = DnaSequencesBulkGet(
            dna_sequences=dna_sequences,
        )

        return dna_sequences_bulk_get
