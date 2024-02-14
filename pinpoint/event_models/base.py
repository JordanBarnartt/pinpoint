from typing import Any

from pydantic import BaseModel, ConfigDict, create_model


Event = dict[str, Any]


class EventModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class EventProtocol(EventModel):
    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    @classmethod
    def enrich_model(cls, **new_attrs: Any) -> "type[EventProtocol]":
        new_attrs = {k: (type(v), v) for k, v in new_attrs.items()}
        new_model = create_model(cls.__name__, __base__=cls, **new_attrs)
        return new_model
