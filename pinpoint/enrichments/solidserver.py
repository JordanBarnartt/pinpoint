from functools import cache
from typing import Any

import SOLIDserverRest  # type: ignore
from pydantic import BaseModel, Field
from SOLIDserverRest import adv as sdsadv  # type: ignore

from pinpoint.enrichments import utils
from pinpoint.enrichments.base import EnrichmentProtocol
from pinpoint.event_models.base import Event


class SolidserverMetadata(BaseModel):
    hostname: str = Field(alias="name")
    mac_address: str = Field(alias="mac_addr")
    subnet_name: str = Field(alias="subnet_name")


class SolidserverMetaEnrichment(EnrichmentProtocol):
    def __init__(self, pivot: str, host: str, username: str, password: str):
        self.sds = sdsadv.SDS(host, username, password)
        self.pivot = pivot

    @cache
    def _sds_hostaddr_query(self, table: str, hostname: str) -> dict[str, Any]:
        self.sds.connect(method="native")
        params = {
            "WHERE": f"hostaddr = '{hostname}'",
        }
        response = self.sds.query(table, params=params)
        return response[0]

    def enrich(self, event: Event, namespace: str = "") -> Event:
        pivot_value = utils.extract_pivot(event, self.pivot)
        try:
            response = self._sds_hostaddr_query(
                table="ip_address_list", hostname=pivot_value
            )
            metadata = SolidserverMetadata(**response).model_dump()
        except SOLIDserverRest.Exception.SDSEmptyError:
            metadata = {}
        event["Solidserver"] = metadata

        return event
