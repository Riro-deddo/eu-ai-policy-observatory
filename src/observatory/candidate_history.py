from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime


SNAPSHOT_FIELDS = (
    "decision", "decision_reason", "document_id",
    "merged_into_document_id", "reviewed_at", "reviewed_by",
)


def reopen_candidate(candidate: Mapping[str, object], *, reason: str,
                     reviewed_at: str, reviewed_by: str) -> dict[str, object]:
    if candidate.get("decision") != "excluded":
        raise ValueError("Only excluded candidates can be reopened by this operation.")
    if not reason.strip() or not reviewed_by.strip():
        raise ValueError("A reason and an accurately named reviewer are required.")
    current_time = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
    if current_time.tzinfo is None:
        raise ValueError("A timezone-aware review timestamp is required.")
    previous_time = candidate.get("reviewed_at")
    if isinstance(previous_time, str):
        previous = datetime.fromisoformat(previous_time.replace("Z", "+00:00"))
        if previous.tzinfo is None or current_time < previous:
            raise ValueError("Review history cannot be backdated.")
    result = deepcopy(dict(candidate))
    history = result.get("decision_history", [])
    if not isinstance(history, list):
        raise ValueError("decision_history must be an array.")
    history.append({key: deepcopy(candidate[key]) for key in SNAPSHOT_FIELDS})
    result.update(decision="pending", decision_reason=reason,
                  document_id=None, merged_into_document_id=None,
                  reviewed_at=reviewed_at, reviewed_by=reviewed_by,
                  decision_history=history)
    return result
