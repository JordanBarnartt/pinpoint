import datetime
import ipaddress
from typing import Any

from elasticsearch import Elasticsearch
from pydantic import AliasPath, Field

from pinpoint.enrichments import utils
from pinpoint.enrichments.base import EnrichmentProtocol
from pinpoint.event_models.base import EventProtocol, Event

_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class Point(EventProtocol):
    lat: float
    lon: float


class Geo(EventProtocol):
    city_name: str | None = None
    continent_name: str
    country_iso_code: str
    country_name: str
    location: Point
    region_iso_code: str | None = None
    region_name: str | None = None


class SrcDst(EventProtocol):
    address: ipaddress.IPv4Address | ipaddress.IPv6Address
    port: int
    organization_name: str = Field(
        validation_alias=AliasPath("as", "organization", "name")
    )
    geo: Geo


class SuricataEvent(EventProtocol):
    timestamp: datetime.datetime = Field(validation_alias="@timestamp")
    source: SrcDst
    destination: SrcDst
    alert_category: str = Field(
        validation_alias=AliasPath("suricata", "eve", "alert", "category")
    )
    alert_signature: str = Field(
        validation_alias=AliasPath("suricata", "eve", "alert", "signature")
    )
    alert_signature_id: int = Field(
        validation_alias=AliasPath("suricata", "eve", "alert", "signature_id")
    )
    alert_payload: str = Field(
        validation_alias=AliasPath("suricata", "eve", "payload_printable")
    )


class SuricataLogEnrichment(EnrichmentProtocol):
    def __init__(
        self,
        pivot: str,
        field: str,
        host: str,
        api_key: tuple[str, str],
        index: str,
        time_range: tuple[datetime.datetime, datetime.datetime] | None = None,
    ):
        self.client = Elasticsearch(hosts=host, api_key=api_key)
        self.pivot = pivot
        self.field = field
        self.index = index
        if time_range:
            self.start_time: str | None = time_range[0].strftime(_TIMESTAMP_FORMAT)
            self.end_time: str | None = time_range[1].strftime(_TIMESTAMP_FORMAT)
        else:
            self.start_time = None
            self.end_time = None

    def enrich(self, event: Event, namespace: str = "suricata") -> Event:
        pivot_value = utils.extract_pivot(event, self.pivot)

        query: dict[str, Any] = {"query": {}}
        query["query"]["term"] = {
            self.field: str(pivot_value),
        }

        if self.start_time and self.end_time:
            query["query"]["range"] = {
                "timestamp": {
                    "gte": self.start_time,
                    "lte": self.end_time,
                }
            }

        search_results = self.client.search(index=self.index, body=query)

        event[namespace] = [
            SuricataEvent(**event["_source"]).model_dump()
            for event in search_results["hits"]["hits"]
        ]

        return event
