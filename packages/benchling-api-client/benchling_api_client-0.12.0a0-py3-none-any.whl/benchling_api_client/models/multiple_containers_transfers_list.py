from typing import Any, Dict, List

import attr

from ..models.multiple_containers_transfer import MultipleContainersTransfer


@attr.s(auto_attribs=True)
class MultipleContainersTransfersList:
    """  """

    transfers: List[MultipleContainersTransfer]

    def to_dict(self) -> Dict[str, Any]:
        transfers = []
        for transfers_item_data in self.transfers:
            transfers_item = transfers_item_data.to_dict()

            transfers.append(transfers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "transfers": transfers,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "MultipleContainersTransfersList":
        d = src_dict.copy()
        transfers = []
        _transfers = d.pop("transfers")
        for transfers_item_data in _transfers:
            transfers_item = MultipleContainersTransfer.from_dict(transfers_item_data)

            transfers.append(transfers_item)

        multiple_containers_transfers_list = MultipleContainersTransfersList(
            transfers=transfers,
        )

        return multiple_containers_transfers_list
