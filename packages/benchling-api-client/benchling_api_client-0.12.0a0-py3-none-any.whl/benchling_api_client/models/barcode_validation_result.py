from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class BarcodeValidationResult:
    """  """

    barcode: str
    is_valid: bool
    message: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        barcode = self.barcode
        is_valid = self.is_valid
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "barcode": barcode,
                "isValid": is_valid,
                "message": message,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BarcodeValidationResult":
        d = src_dict.copy()
        barcode = d.pop("barcode")

        is_valid = d.pop("isValid")

        message = d.pop("message")

        barcode_validation_result = BarcodeValidationResult(
            barcode=barcode,
            is_valid=is_valid,
            message=message,
        )

        return barcode_validation_result
