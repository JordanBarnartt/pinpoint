import datetime
import ipaddress

from pinpoint.event_sources.base import EventSourceProtocol
from pinpoint.enrichments.base import EnrichmentProtocol
from pinpoint.event_models.base import EventModel, EventProtocol


class PinpointPipeline:
    def __init__(
        self,
        events_source: EventSourceProtocol,
        home_ips: (
            list[
                ipaddress.IPv4Address
                | ipaddress.IPv4Network
                | ipaddress.IPv6Address
                | ipaddress.IPv6Network
            ]
            | None
        ) = None,
        time_differential: tuple[datetime.timedelta, datetime.timedelta] | None = (
            datetime.timedelta(minutes=5),
            datetime.timedelta(minutes=5),
        ),
        event_enrichments: list[EnrichmentProtocol] | None = None,
        enrichments: (
            tuple[str, EnrichmentProtocol, list[EnrichmentProtocol]] | None
        ) = None,
    ):
        self.events_source = events_source
        self.time_differential = time_differential
        self.enrichments = enrichments
        self.events: list[EventModel] = []

    def process(self) -> EventProtocol:
        events = self.events_source.get_events()

        return events
