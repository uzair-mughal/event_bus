from datetime import datetime
from event_bus.src.errors import TypeNotSerializableError


def serialize(obj: object) -> str:
    if isinstance(obj, datetime):
        return datetime.strftime(obj, "%Y-%m-%dT%H:%M:%S")

    raise TypeNotSerializableError(obj=str(type(obj)))


def deserialize(obj: dict) -> dict:
    for key, value in obj.items():
        try:
            obj.update(
                {
                    key: datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").replace(microsecond=0),
                }
            )
        except Exception:
            pass

    return obj
