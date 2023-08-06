from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class AutomationOutputProcessorUpdate:
    """  """

    file_id: str

    def to_dict(self) -> Dict[str, Any]:
        file_id = self.file_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fileId": file_id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AutomationOutputProcessorUpdate":
        d = src_dict.copy()
        file_id = d.pop("fileId")

        automation_output_processor_update = AutomationOutputProcessorUpdate(
            file_id=file_id,
        )

        return automation_output_processor_update
