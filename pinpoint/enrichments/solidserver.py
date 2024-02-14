from SOLIDserverRest import adv as sdsadv  # type: ignore

from pydantic import BaseModel

from pinpoint.event_models.base import EventProtocol


class SolidserverMetadata(BaseModel):
    _attrs: list[str] = ["hostname"]
    hostname: str


class SolidserverMetaEnrichment:
    def __init__(self, pivot: str, host: str, username: str, password: str):
        self.sds = sdsadv.SDS(host, username, password)
        self.pivot = pivot

    def enrich(self, event: EventProtocol):
        self.sds.connect(method="native")
        params = {
            "WHERE": f"hostaddr = '{event[self.pivot]}'",
        }
        response = self.sds.query("ip_address_list", params=params)
        metadata = SolidserverMetadata(**response)
        event.add_metadata(metadata.model_dump())
