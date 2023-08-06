from typing import Any, Dict

import attr

from ..models.user_summary import UserSummary


@attr.s(auto_attribs=True)
class RequestUserAssignee:
    """  """

    user: UserSummary

    def to_dict(self) -> Dict[str, Any]:
        user = self.user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "user": user,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestUserAssignee":
        d = src_dict.copy()
        user = UserSummary.from_dict(d.pop("user"))

        request_user_assignee = RequestUserAssignee(
            user=user,
        )

        return request_user_assignee
