from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class RequestBase:
    """ A request is an ask to perform a service, e.g. produce a sample or perform assays on a sample. Requests are usually placed to another team or individual who specializes in performing the service. """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestBase":
        src_dict.copy()
        request_base = RequestBase()

        return request_base
