from copy import deepcopy

import pytest

from observatory.candidate_history import reopen_candidate


def test_reopen_preserves_prior_decision_without_mutation():
    candidate = {
        "id": "audit-example", "decision": "excluded",
        "decision_reason": "The English file was not verified.",
        "document_id": None, "merged_into_document_id": None,
        "reviewed_at": "2026-09-04T00:00:00Z", "reviewed_by": "Prior reviewer",
    }
    original = deepcopy(candidate)
    result = reopen_candidate(
        candidate, reason="Official publication identity needs further verification.",
        reviewed_at="2026-09-05T12:00:00Z", reviewed_by="Test reviewer",
    )
    assert candidate == original
    assert result["decision"] == "pending"
    assert result["id"] == candidate["id"]
    assert result["decision_history"] == [{
        key: original[key] for key in (
            "decision", "decision_reason", "document_id",
            "merged_into_document_id", "reviewed_at", "reviewed_by",
        )
    }]
    with pytest.raises(ValueError):
        reopen_candidate(result, reason="Again", reviewed_at="2026-09-05T13:00:00Z",
                         reviewed_by="Test reviewer")


@pytest.mark.parametrize("candidate_patch,argument_patch", [
    ({}, {"reason": " "}),
    ({}, {"reviewed_by": " "}),
    ({}, {"reviewed_at": "2026-09-05T12:00:00"}),
    ({}, {"reviewed_at": "2026-09-03T12:00:00Z"}),
    ({"decision": "included"}, {}),
    ({"decision_history": {}}, {}),
])
def test_invalid_reopening_does_not_mutate_input(candidate_patch, argument_patch):
    candidate = {
        "id": "audit-example", "decision": "excluded",
        "decision_reason": "Prior decision", "document_id": None,
        "merged_into_document_id": None,
        "reviewed_at": "2026-09-04T00:00:00Z", "reviewed_by": "Prior reviewer",
    }
    candidate.update(candidate_patch)
    original = deepcopy(candidate)
    arguments = {
        "reason": "Requires review", "reviewed_at": "2026-09-05T12:00:00Z",
        "reviewed_by": "Test reviewer",
    }
    arguments.update(argument_patch)
    with pytest.raises(ValueError):
        reopen_candidate(candidate, **arguments)
    assert candidate == original
