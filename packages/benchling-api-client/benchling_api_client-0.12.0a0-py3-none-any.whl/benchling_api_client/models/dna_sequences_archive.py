from typing import Any, Dict, List, cast

import attr

from ..models.dna_sequences_archive_reason import DnaSequencesArchiveReason


@attr.s(auto_attribs=True)
class DnaSequencesArchive:
    """The request body for archiving DNA sequences."""

    reason: DnaSequencesArchiveReason
    dna_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        dna_sequence_ids = self.dna_sequence_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "dnaSequenceIds": dna_sequence_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DnaSequencesArchive":
        d = src_dict.copy()
        reason = DnaSequencesArchiveReason(d.pop("reason"))

        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds"))

        dna_sequences_archive = DnaSequencesArchive(
            reason=reason,
            dna_sequence_ids=dna_sequence_ids,
        )

        return dna_sequences_archive
