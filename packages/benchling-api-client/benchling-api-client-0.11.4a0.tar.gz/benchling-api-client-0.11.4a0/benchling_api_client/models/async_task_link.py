from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class AsyncTaskLink:
    """  """

    task_id: str

    def to_dict(self) -> Dict[str, Any]:
        task_id = self.task_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "taskId": task_id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AsyncTaskLink":
        d = src_dict.copy()
        task_id = d.pop("taskId")

        async_task_link = AsyncTaskLink(
            task_id=task_id,
        )

        return async_task_link
