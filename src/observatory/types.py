from dataclasses import dataclass


ENTITY_DIRECTORIES = (
    "policies",
    "documents",
    "events",
    "concepts",
    "institutions",
    "relationships",
    "sources",
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    record_path: str
    field: str
    message: str
