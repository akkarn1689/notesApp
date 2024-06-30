def note_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "desc": item["desc"],
        "important": item["important"]
    }


def notes_entity(items) -> list:
    return [note_entity(item) for item in items]
