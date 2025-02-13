from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar


from classes.events.event import (
    T,
    event,
)
from classes.repositories.event_repo import EventRepo

A = TypeVar("A", bound="Aggregate")


@dataclass(kw_only=True)
class Aggregate:
    id: int
    type: str
    create_date: datetime = field(default_factory=datetime.now)
    version: int
    event_store = EventRepo()
    _initalised = False

    @event("AggregateCreated")
    def __post_init__(self):
        self._initalised = True

    def add_event(self, event_instance: T):
        self.event_store.store_event(event_instance)
        return self

    @classmethod
    def load_events(
        self,
        key: str,
    ):
        events = self.event_store.get_events(key)
        return events

    @property
    def initalised(self):
        return self._initalised
