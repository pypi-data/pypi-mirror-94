from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class Pagination:
    """  """

    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Pagination":
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        pagination = Pagination(
            next_token=next_token,
        )

        return pagination
