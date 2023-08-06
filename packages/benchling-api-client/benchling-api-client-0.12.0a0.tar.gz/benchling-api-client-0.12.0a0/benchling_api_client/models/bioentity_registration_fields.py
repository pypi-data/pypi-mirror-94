from typing import Any, Dict, Union

import attr

from ..models.naming_strategy import NamingStrategy
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class BioentityRegistrationFields:
    """  """

    registry_id: Union[Unset, str] = UNSET
    naming_strategy: Union[Unset, NamingStrategy] = UNSET
    entity_registry_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        registry_id = self.registry_id
        naming_strategy: Union[Unset, int] = UNSET
        if not isinstance(self.naming_strategy, Unset):
            naming_strategy = self.naming_strategy.value

        entity_registry_id = self.entity_registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if naming_strategy is not UNSET:
            field_dict["namingStrategy"] = naming_strategy
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BioentityRegistrationFields":
        d = src_dict.copy()
        registry_id = d.pop("registryId", UNSET)

        naming_strategy = None
        _naming_strategy = d.pop("namingStrategy", UNSET)
        if _naming_strategy is not None:
            naming_strategy = NamingStrategy(_naming_strategy)

        entity_registry_id = d.pop("entityRegistryId", UNSET)

        bioentity_registration_fields = BioentityRegistrationFields(
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            entity_registry_id=entity_registry_id,
        )

        return bioentity_registration_fields
