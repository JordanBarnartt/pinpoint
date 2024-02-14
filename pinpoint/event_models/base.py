from pydantic import BaseModel

from typing import Any


class EventModel(BaseModel):
    pass


class EventProtocol(EventModel):
    def add_metadata(self, metadata: dict[str, Any]):
        for key, value in metadata.items():
            setattr(self, key, value)
