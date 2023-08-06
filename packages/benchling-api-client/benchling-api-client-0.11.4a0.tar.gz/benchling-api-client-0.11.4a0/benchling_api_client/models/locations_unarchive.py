from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class LocationsUnarchive:
    """  """

    location_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        location_ids = self.location_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "locationIds": location_ids,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "LocationsUnarchive":
        d = src_dict.copy()
        location_ids = cast(List[str], d.pop("locationIds"))

        locations_unarchive = LocationsUnarchive(
            location_ids=location_ids,
        )

        return locations_unarchive
