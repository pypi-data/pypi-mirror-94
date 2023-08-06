from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class LabelTemplate:
    """  """

    id: str
    name: str
    zpl_template: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        zpl_template = self.zpl_template

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "zplTemplate": zpl_template,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "LabelTemplate":
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        zpl_template = d.pop("zplTemplate")

        label_template = LabelTemplate(
            id=id,
            name=name,
            zpl_template=zpl_template,
        )

        return label_template
