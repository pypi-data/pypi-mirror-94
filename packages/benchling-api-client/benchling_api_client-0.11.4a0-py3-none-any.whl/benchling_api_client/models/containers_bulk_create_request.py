from typing import Any, Dict, List

import attr

from ..models.container_create import ContainerCreate


@attr.s(auto_attribs=True)
class ContainersBulkCreateRequest:
    """  """

    containers: List[ContainerCreate]

    def to_dict(self) -> Dict[str, Any]:
        containers = []
        for containers_item_data in self.containers:
            containers_item = containers_item_data.to_dict()

            containers.append(containers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containers": containers,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ContainersBulkCreateRequest":
        d = src_dict.copy()
        containers = []
        _containers = d.pop("containers")
        for containers_item_data in _containers:
            containers_item = ContainerCreate.from_dict(containers_item_data)

            containers.append(containers_item)

        containers_bulk_create_request = ContainersBulkCreateRequest(
            containers=containers,
        )

        return containers_bulk_create_request
