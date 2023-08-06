from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class ExportItemRequest:
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
    def from_dict(src_dict: Dict[str, Any]) -> "ExportItemRequest":
        d = src_dict.copy()
        id = d.pop("id")

        export_item_request = ExportItemRequest(
            id=id,
        )

        return export_item_request
