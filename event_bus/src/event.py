import json
import hashlib
from datetime import date, datetime
from event_bus.src.errors import TypeNotSerializableError


class Event:
    def __init__(self, name: str, properties: dict, created_at: datetime = None, retries: int = 0, event_id: str = ""):
        self._name = name
        self._retries = retries
        self._properties = properties
        self._created_at = created_at or datetime.now()

        stringified_event = json.dumps(
            {"header": {"name": self.name}, "body": self.properties}, default=self._serialize, indent=2, sort_keys=True
        )

        self._id = hashlib.md5(stringified_event.encode("utf-8")).hexdigest()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def properties(self):
        return self._properties

    @property
    def created_at(self):
        return self._created_at

    @property
    def retries(self):
        return self._retries

    def increment_retries(self):
        self._retries += 1

    def decrement_retries(self):
        self._retries -= 1

    def to_json(self):
        event = {
            "header": {"id": self.id, "name": self.name, "created_at": self.created_at, "retries": self.retries},
            "body": self.properties,
        }

        return json.dumps(event, default=self._serialize, indent=2, sort_keys=True)

    def _serialize(self, obj):
        if isinstance(obj, (datetime, date)):
            return datetime.strftime(obj, "%Y-%m-%d %H:%M:%S")

        raise TypeNotSerializableError(type(obj))
