from typing import Any, Dict, List, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AutomationFileAutomationFileConfig:
    """  """

    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AutomationFileAutomationFileConfig":
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        automation_file_automation_file_config = AutomationFileAutomationFileConfig(
            name=name,
        )

        automation_file_automation_file_config.additional_properties = d
        return automation_file_automation_file_config

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
