from typing import Any, Dict, Union

import attr

from ..models.measurement import Measurement
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class ContainerTransferBase:
    """  """

    transfer_volume: Measurement
    source_entity_id: Union[Unset, str] = UNSET
    source_batch_id: Union[Unset, str] = UNSET
    source_container_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        transfer_volume = self.transfer_volume.to_dict()

        source_entity_id = self.source_entity_id
        source_batch_id = self.source_batch_id
        source_container_id = self.source_container_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "transferVolume": transfer_volume,
            }
        )
        if source_entity_id is not UNSET:
            field_dict["sourceEntityId"] = source_entity_id
        if source_batch_id is not UNSET:
            field_dict["sourceBatchId"] = source_batch_id
        if source_container_id is not UNSET:
            field_dict["sourceContainerId"] = source_container_id

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ContainerTransferBase":
        d = src_dict.copy()
        transfer_volume = Measurement.from_dict(d.pop("transferVolume"))

        source_entity_id = d.pop("sourceEntityId", UNSET)

        source_batch_id = d.pop("sourceBatchId", UNSET)

        source_container_id = d.pop("sourceContainerId", UNSET)

        container_transfer_base = ContainerTransferBase(
            transfer_volume=transfer_volume,
            source_entity_id=source_entity_id,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
        )

        return container_transfer_base
