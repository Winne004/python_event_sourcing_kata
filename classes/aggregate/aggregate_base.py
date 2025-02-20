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
    _event_store: EventRepo | None = None
    _initalised = False

    @event("AggregateCreated")
    def __post_init__(self):
        self.name = self.__class__.__name__
        self._initalised = True
        if not self._event_store:
            self.event_store = EventRepo()

    def add_event(self, event_instance: T):
        self._event_store.store_event(event_instance)
        return self

    @classmethod
    def load_events(
        self,
        key: str,
        event_store: EventRepo,
    ):
        events = event_store.get_events(key)
        return events

    @property
    def initalised(self):
        return self._initalised
