from typing import Any, Dict, List, Union

import attr

from ..models.custom_entity import CustomEntity
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class CustomEntitiesList:
    """  """

    custom_entities: Union[Unset, List[CustomEntity]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        custom_entities: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.custom_entities, Unset):
            custom_entities = []
            for custom_entities_item_data in self.custom_entities:
                custom_entities_item = custom_entities_item_data.to_dict()

                custom_entities.append(custom_entities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if custom_entities is not UNSET:
            field_dict["customEntities"] = custom_entities

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "CustomEntitiesList":
        d = src_dict.copy()
        custom_entities = []
        _custom_entities = d.pop("customEntities", UNSET)
        for custom_entities_item_data in _custom_entities or []:
            custom_entities_item = CustomEntity.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        custom_entities_list = CustomEntitiesList(
            custom_entities=custom_entities,
        )

        return custom_entities_list
