from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class Mixture:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Mixture":
        src_dict.copy()
        mixture = Mixture()

        return mixture
