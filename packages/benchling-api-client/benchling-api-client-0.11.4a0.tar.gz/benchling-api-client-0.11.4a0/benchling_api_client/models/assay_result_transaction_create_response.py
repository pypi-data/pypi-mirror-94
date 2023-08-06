from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class AssayResultTransactionCreateResponse:
    """  """

    id: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayResultTransactionCreateResponse":
        d = src_dict.copy()
        id = d.pop("id")

        assay_result_transaction_create_response = AssayResultTransactionCreateResponse(
            id=id,
        )

        return assay_result_transaction_create_response
