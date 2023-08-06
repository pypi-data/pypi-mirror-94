from typing import Any, Dict

import attr

from ..models.team_summary import TeamSummary


@attr.s(auto_attribs=True)
class RequestTeamAssignee:
    """  """

    team: TeamSummary

    def to_dict(self) -> Dict[str, Any]:
        team = self.team.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "team": team,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestTeamAssignee":
        d = src_dict.copy()
        team = TeamSummary.from_dict(d.pop("team"))

        request_team_assignee = RequestTeamAssignee(
            team=team,
        )

        return request_team_assignee
