import abc

from pinpoint.event_models.base import Event


class EnrichmentProtocol(abc.ABC):

    @abc.abstractmethod
    def enrich(self, event: Event, namespace: str = ""): ...
