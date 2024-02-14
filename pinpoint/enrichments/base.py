import abc

from pinpoint.event_models.base import EventProtocol


class EnrichmentProtocol(abc.ABC):

    @abc.abstractmethod
    def enrich(self, event: EventProtocol): ...
