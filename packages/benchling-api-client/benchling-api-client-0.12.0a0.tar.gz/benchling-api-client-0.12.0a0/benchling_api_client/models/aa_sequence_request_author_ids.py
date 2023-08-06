from typing import Any, Dict, List, Union, cast

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AaSequenceRequestAuthorIds:
    """  """

    author_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        author_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.author_ids, Unset):
            author_ids = self.author_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AaSequenceRequestAuthorIds":
        d = src_dict.copy()
        author_ids = cast(List[str], d.pop("authorIds", UNSET))

        aa_sequence_request_author_ids = AaSequenceRequestAuthorIds(
            author_ids=author_ids,
        )

        return aa_sequence_request_author_ids
