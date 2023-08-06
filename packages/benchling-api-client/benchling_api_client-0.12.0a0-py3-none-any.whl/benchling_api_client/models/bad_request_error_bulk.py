from typing import Any, Dict, Union

import attr

from ..models.bad_request_error_bulk_error import BadRequestErrorBulkError
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class BadRequestErrorBulk:
    """  """

    error: Union[Unset, BadRequestErrorBulkError] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BadRequestErrorBulk":
        d = src_dict.copy()
        error: Union[Unset, BadRequestErrorBulkError] = UNSET
        _error = d.pop("error", UNSET)
        if not isinstance(_error, Unset):
            error = BadRequestErrorBulkError.from_dict(_error)

        bad_request_error_bulk = BadRequestErrorBulk(
            error=error,
        )

        return bad_request_error_bulk
