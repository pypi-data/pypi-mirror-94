from typing import Any, Dict, List

import attr

from ..models.request import Request


@attr.s(auto_attribs=True)
class RequestsBulkGet:
    """  """

    requests: List[Request]

    def to_dict(self) -> Dict[str, Any]:
        requests = []
        for requests_item_data in self.requests:
            requests_item = requests_item_data.to_dict()

            requests.append(requests_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "requests": requests,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestsBulkGet":
        d = src_dict.copy()
        requests = []
        _requests = d.pop("requests")
        for requests_item_data in _requests:
            requests_item = Request.from_dict(requests_item_data)

            requests.append(requests_item)

        requests_bulk_get = RequestsBulkGet(
            requests=requests,
        )

        return requests_bulk_get
