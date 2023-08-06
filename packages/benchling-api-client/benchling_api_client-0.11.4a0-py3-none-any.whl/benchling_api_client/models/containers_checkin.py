from typing import Any, Dict, List, Union, cast

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class ContainersCheckin:
    """  """

    container_ids: List[str]
    comments: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerIds": container_ids,
            }
        )
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ContainersCheckin":
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds"))

        comments = d.pop("comments", UNSET)

        containers_checkin = ContainersCheckin(
            container_ids=container_ids,
            comments=comments,
        )

        return containers_checkin
