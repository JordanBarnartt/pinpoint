import datetime
from typing import Any

from elasticsearch import Elasticsearch

from pinpoint.event_models.zeek_intel import ZeekIntelEvent
from pinpoint.event_sources.base import EventSourceProtocol
from pinpoint.event_models.base import EventProtocol

_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class ZeekIntelEventSource(EventSourceProtocol):
    def __init__(
        self,
        host: str,
        api_key: tuple[str, str],
        index: str,
        event_id: str | None = None,
        time_range: tuple[datetime.datetime, datetime.datetime] | None = None,
    ):
        self.client = Elasticsearch(hosts=host, api_key=api_key)
        self.index = index
        self.event_id = event_id
        if time_range:
            self.start_time: str | None = time_range[0].strftime(_TIMESTAMP_FORMAT)
            self.end_time: str | None = time_range[1].strftime(_TIMESTAMP_FORMAT)
        else:
            self.start_time = None
            self.end_time = None

    def get_events(self) -> list[EventProtocol]:
        query: dict[str, Any] = {"query": {}}
        if self.event_id:
            query["query"]["term"] = {
                "_id": self.event_id,
            }

        if self.start_time and self.end_time:
            query["query"]["range"] = {
                "timestamp": {
                    "gte": self.start_time,
                    "lte": self.end_time,
                }
            }

        search_results = self.client.search(index=self.index, body=query)
        return [
            ZeekIntelEvent(**event["_source"])
            for event in search_results["hits"]["hits"]
        ]
