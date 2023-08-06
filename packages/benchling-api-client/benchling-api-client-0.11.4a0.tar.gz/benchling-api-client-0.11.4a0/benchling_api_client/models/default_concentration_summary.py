from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class DefaultConcentrationSummary:
    """  """

    units: Union[Unset, str] = UNSET
    value: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        units = self.units
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if units is not UNSET:
            field_dict["units"] = units
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DefaultConcentrationSummary":
        d = src_dict.copy()
        units = d.pop("units", UNSET)

        value = d.pop("value", UNSET)

        default_concentration_summary = DefaultConcentrationSummary(
            units=units,
            value=value,
        )

        return default_concentration_summary
