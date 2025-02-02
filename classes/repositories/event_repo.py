from dataclasses import dataclass, field
from typing import Dict, List

from classes.dataclasses.event import T
from classes.repositories.event_manager import EventManager


@dataclass
class EventRepo(EventManager):
    """Repository for storing events."""

    events: Dict[str, List[T]] = field(default_factory=dict)

    def store_event(self, event: T):
        """Store an event in the repository."""
        if event.partition_key not in self.events:
            self.events[event.partition_key] = []
        self.events[event.partition_key].append(event)
        self.notify(event.name, event)

    def get_events(self, partition_key: str) -> List[T]:
        """Get all events for a partition key."""
        return sorted(self.events.get(partition_key, []), key=lambda e: e.timestamp)
