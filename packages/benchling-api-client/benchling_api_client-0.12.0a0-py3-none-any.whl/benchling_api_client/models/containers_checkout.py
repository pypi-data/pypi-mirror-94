from typing import Any, Dict, List, Union, cast

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class ContainersCheckout:
    """  """

    container_ids: List[str]
    assignee_id: str
    comments: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        assignee_id = self.assignee_id
        comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerIds": container_ids,
                "assigneeId": assignee_id,
            }
        )
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ContainersCheckout":
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds"))

        assignee_id = d.pop("assigneeId")

        comments = d.pop("comments", UNSET)

        containers_checkout = ContainersCheckout(
            container_ids=container_ids,
            assignee_id=assignee_id,
            comments=comments,
        )

        return containers_checkout
