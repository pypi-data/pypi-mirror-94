from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class RequestWriteTeamAssignee:
    """  """

    team_id: str

    def to_dict(self) -> Dict[str, Any]:
        team_id = self.team_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "teamId": team_id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestWriteTeamAssignee":
        d = src_dict.copy()
        team_id = d.pop("teamId")

        request_write_team_assignee = RequestWriteTeamAssignee(
            team_id=team_id,
        )

        return request_write_team_assignee
