from typing import Any, Dict, List

import attr

from ..models.requests_task import RequestsTask


@attr.s(auto_attribs=True)
class RequestsTasksBulkUpdateResponse:
    """  """

    tasks: List[RequestsTask]

    def to_dict(self) -> Dict[str, Any]:
        tasks = []
        for tasks_item_data in self.tasks:
            tasks_item = tasks_item_data.to_dict()

            tasks.append(tasks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "tasks": tasks,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestsTasksBulkUpdateResponse":
        d = src_dict.copy()
        tasks = []
        _tasks = d.pop("tasks")
        for tasks_item_data in _tasks:
            tasks_item = RequestsTask.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        requests_tasks_bulk_update_response = RequestsTasksBulkUpdateResponse(
            tasks=tasks,
        )

        return requests_tasks_bulk_update_response
