from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class Samples:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Samples":
        src_dict.copy()
        samples = Samples()

        return samples
