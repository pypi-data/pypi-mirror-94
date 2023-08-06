from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class WarehouseCredentialsCreate:
    """  """

    expires_in: int

    def to_dict(self) -> Dict[str, Any]:
        expires_in = self.expires_in

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expiresIn": expires_in,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "WarehouseCredentialsCreate":
        d = src_dict.copy()
        expires_in = d.pop("expiresIn")

        warehouse_credentials_create = WarehouseCredentialsCreate(
            expires_in=expires_in,
        )

        return warehouse_credentials_create
