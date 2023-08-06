from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class DnaSequenceRequestRegistryFields:
    """  """

    entity_registry_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entity_registry_id = self.entity_registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DnaSequenceRequestRegistryFields":
        d = src_dict.copy()
        entity_registry_id = d.pop("entityRegistryId", UNSET)

        dna_sequence_request_registry_fields = DnaSequenceRequestRegistryFields(
            entity_registry_id=entity_registry_id,
        )

        return dna_sequence_request_registry_fields
