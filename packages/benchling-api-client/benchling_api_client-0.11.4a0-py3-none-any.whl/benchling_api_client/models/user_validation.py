from typing import Any, Dict, Union

import attr

from ..models.user_validation_validation_status import UserValidationValidationStatus
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class UserValidation:
    """  """

    validation_status: Union[Unset, UserValidationValidationStatus] = UNSET
    validation_comment: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        validation_status: Union[Unset, int] = UNSET
        if not isinstance(self.validation_status, Unset):
            validation_status = self.validation_status.value

        validation_comment = self.validation_comment

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "UserValidation":
        d = src_dict.copy()
        validation_status = None
        _validation_status = d.pop("validationStatus", UNSET)
        if _validation_status is not None:
            validation_status = UserValidationValidationStatus(_validation_status)

        validation_comment = d.pop("validationComment", UNSET)

        user_validation = UserValidation(
            validation_status=validation_status,
            validation_comment=validation_comment,
        )

        return user_validation
