from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class CreateIntoRegistry:
    """  """

    registry_id: Union[Unset, str] = UNSET
    naming_strategy: Union[Unset, str] = UNSET
    entity_registry_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        registry_id = self.registry_id
        naming_strategy = self.naming_strategy
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
    def from_dict(src_dict: Dict[str, Any]) -> "CreateIntoRegistry":
        d = src_dict.copy()
        registry_id = d.pop("registryId", UNSET)

        naming_strategy = d.pop("namingStrategy", UNSET)

        entity_registry_id = d.pop("entityRegistryId", UNSET)

        create_into_registry = CreateIntoRegistry(
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            entity_registry_id=entity_registry_id,
        )

        return create_into_registry
