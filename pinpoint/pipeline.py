import datetime
import ipaddress

from pinpoint.event_sources.base import EventSourceProtocol
from pinpoint.enrichments.base import EnrichmentProtocol
from pinpoint.event_models.base import EventModel, Event


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
            datetime.timedelta(days=1),
            datetime.timedelta(days=1),
        ),
        meta_enrichments: list[EnrichmentProtocol] | None = None,
        log_enrichments: (
            list[tuple[str, EnrichmentProtocol, list[EnrichmentProtocol]]] | None
        ) = None,
    ):
        self.events_source = events_source
        self.time_differential = time_differential
        self.meta_enrichments = meta_enrichments
        self.log_enrichments = log_enrichments
        self.events: list[EventModel] = []

    def process(self) -> list[Event]:
        events = self.events_source.get_events()

        for i, event in enumerate(events):
            if self.meta_enrichments:
                for event_enrichment in self.meta_enrichments:
                    events[i] = event_enrichment.enrich(event)
            if self.log_enrichments:
                for namespace, log_enrichment, meta_enrichments in self.log_enrichments:
                    events[i] = log_enrichment.enrich(event, namespace)
                    for meta_enrichment in meta_enrichments:
                        events[i] = meta_enrichment.enrich(event)

        return events
