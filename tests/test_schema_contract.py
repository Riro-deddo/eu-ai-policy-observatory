from observatory.types import ENTITY_DIRECTORIES, ValidationIssue


def test_entity_directories_are_explicit_and_stable():
    assert ENTITY_DIRECTORIES == (
        "policies",
        "documents",
        "events",
        "concepts",
        "institutions",
        "relationships",
        "sources",
    )


def test_validation_issue_is_immutable():
    issue = ValidationIssue("required", "documents/example.json", "celex", "Missing CELEX")
    assert issue.code == "required"
    assert issue.record_path.endswith("example.json")
