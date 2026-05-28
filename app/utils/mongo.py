from bson import ObjectId


def serialize_document(document: dict | None) -> dict | None:
    if document is None:
        return None

    serialized = {}

    for key, value in document.items():
        serialized[key] = str(value) if isinstance(value, ObjectId) else value

    return serialized


def serialize_documents(documents: list[dict]) -> list[dict]:
    return [serialize_document(document) for document in documents]
