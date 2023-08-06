from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class AutofillSequences:
    """  """

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
    def from_dict(src_dict: Dict[str, Any]) -> "AutofillSequences":
        d = src_dict.copy()
        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds"))

        autofill_sequences = AutofillSequences(
            dna_sequence_ids=dna_sequence_ids,
        )

        return autofill_sequences
