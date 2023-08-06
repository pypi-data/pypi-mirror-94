from typing import Any, Dict, Union

import attr

from ..models.blob_multipart_create_type import BlobMultipartCreateType
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class BlobMultipartCreate:
    """  """

    name: str
    type: BlobMultipartCreateType
    mime_type: Union[Unset, str] = "application/octet-stream"

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        mime_type = self.mime_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BlobMultipartCreate":
        d = src_dict.copy()
        name = d.pop("name")

        type = BlobMultipartCreateType(d.pop("type"))

        mime_type = d.pop("mimeType", UNSET)

        blob_multipart_create = BlobMultipartCreate(
            name=name,
            type=type,
            mime_type=mime_type,
        )

        return blob_multipart_create
