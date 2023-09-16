import hashlib
import json
from datetime import datetime
from typing import Any, Dict, Optional
from event_bus.src.util import serialize


class Event:
    def __init__(
        self,
        name: str,
        properties: Optional[Dict[str, Any]] = None,
        timestamp: datetime = datetime.now(),
        retries: int = 0,
    ):
        self.__name = name
        self.__timestamp = timestamp.replace(microsecond=0)
        self.__properties = {}
        self.__retries = retries

        if properties:
            for key, value in properties.items():
                if isinstance(value, datetime):
                    self.__properties.update({key: value.replace(microsecond=0)})
                else:
                    self.__properties.update({key: value})

        self.__event: Dict[str, Any] = {
            "name": self.name,
            "properties": self.properties,
        }

        self.__id = hashlib.md5(
            json.dumps(self.__event, default=serialize, indent=2, sort_keys=True).encode("utf-8")
        ).hexdigest()

        self.__event.update({"id": self.id})
        self.__event.update({"timestamp": self.timestamp})
        self.__event.update({"retries": self.retries})

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def properties(self) -> dict:
        return self.__properties

    @property
    def retries(self) -> int:
        return self.__retries

    def to_json(self) -> str:
        return json.dumps(self.__event, default=serialize, indent=2, sort_keys=True)
