import datetime
import ipaddress

from pydantic import Field, AliasPath

from pinpoint.event_models.base import EventProtocol


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


class ZeekIntelEvent(EventProtocol):
    timestamp: datetime.datetime = Field(validation_alias="@timestamp")
    source: SrcDst
    destination: SrcDst
    fuid: str | None = Field(validation_alias=AliasPath("zeek", "intel", "fuid"), default=None)
    matched: list[str] = Field(validation_alias=AliasPath("zeek", "intel", "matched"))
    indicator: str = Field(
        validation_alias=AliasPath("zeek", "intel", "seen", "indicator")
    )
    indicator_type: str = Field(
        validation_alias=AliasPath("zeek", "intel", "seen", "indicator_type")
    )
    seen_where: str = Field(
        validation_alias=AliasPath("zeek", "intel", "seen", "where")
    )
    intel_source: list[str] = Field(validation_alias=AliasPath("zeek", "intel", "sources"))
