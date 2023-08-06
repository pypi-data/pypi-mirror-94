from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class Barcodes:
    """  """

    barcodes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        barcodes = self.barcodes

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "barcodes": barcodes,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Barcodes":
        d = src_dict.copy()
        barcodes = cast(List[str], d.pop("barcodes"))

        barcodes = Barcodes(
            barcodes=barcodes,
        )

        return barcodes
