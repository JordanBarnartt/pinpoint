from pinpoint.event_models.base import EventProtocol


def extract_pivot(event: EventProtocol, pivot: str):
    if "." in pivot:
        pivot_split = pivot.split(".")
        event_attr = event
        for split in pivot_split:
            event_attr = event_attr[split]
    return event_attr
