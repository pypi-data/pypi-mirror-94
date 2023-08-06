from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class BaseError:
    """  """

    message: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    user_message: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        type = self.type
        user_message = self.user_message

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if type is not UNSET:
            field_dict["type"] = type
        if user_message is not UNSET:
            field_dict["userMessage"] = user_message

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BaseError":
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        type = d.pop("type", UNSET)

        user_message = d.pop("userMessage", UNSET)

        base_error = BaseError(
            message=message,
            type=type,
            user_message=user_message,
        )

        return base_error
