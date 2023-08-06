from typing import Any, Dict, List

import attr

from ..models.workflow_stage import WorkflowStage


@attr.s(auto_attribs=True)
class WorkflowStageList:
    """  """

    workflow_stages: List[WorkflowStage]

    def to_dict(self) -> Dict[str, Any]:
        workflow_stages = []
        for workflow_stages_item_data in self.workflow_stages:
            workflow_stages_item = workflow_stages_item_data.to_dict()

            workflow_stages.append(workflow_stages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflowStages": workflow_stages,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "WorkflowStageList":
        d = src_dict.copy()
        workflow_stages = []
        _workflow_stages = d.pop("workflowStages")
        for workflow_stages_item_data in _workflow_stages:
            workflow_stages_item = WorkflowStage.from_dict(workflow_stages_item_data)

            workflow_stages.append(workflow_stages_item)

        workflow_stage_list = WorkflowStageList(
            workflow_stages=workflow_stages,
        )

        return workflow_stage_list
