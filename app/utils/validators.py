from uuid import UUID


def is_uuid(value: str) -> bool:
    try:
        UUID(value)
    except (TypeError, ValueError):
        return False

    return True
