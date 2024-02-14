import abc

from pinpoint.event_models.base import EventProtocol


class EventSourceProtocol(abc.ABC):

    @abc.abstractmethod
    def get_events(self) -> list[EventProtocol]: ...
