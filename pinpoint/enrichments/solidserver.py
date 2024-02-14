from SOLIDserverRest import adv as sdsadv  # type: ignore

from pydantic import BaseModel, Field

from pinpoint.event_models.base import EventProtocol
from pinpoint.enrichments import utils


class SolidserverMetadata(BaseModel):
    solidserver_hostname: str = Field(alias="name")


class SolidserverMetaEnrichment:
    def __init__(self, pivot: str, host: str, username: str, password: str):
        self.sds = sdsadv.SDS(host, username, password)
        self.pivot = pivot

    def enrich(self, event: EventProtocol) -> EventProtocol:
        self.sds.connect(method="native")
        pivot_value = utils.extract_pivot(event, self.pivot)
        params = {
            "WHERE": f"hostaddr = '{pivot_value}'",
        }
        response = self.sds.query("ip_address_list", params=params)[0]
        metadata = SolidserverMetadata(**response).model_dump()
        new_model = event.enrich_model(**metadata)
        updated_event = new_model(**event.model_dump())

        return updated_event
