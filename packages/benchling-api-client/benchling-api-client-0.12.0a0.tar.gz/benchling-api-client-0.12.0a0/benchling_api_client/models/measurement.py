from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class Measurement:
    """  """

    value: Optional[float]
    units: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        units = self.units

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
                "units": units,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Measurement":
        d = src_dict.copy()
        value = d.pop("value")

        units = d.pop("units")

        measurement = Measurement(
            value=value,
            units=units,
        )

        return measurement
