from dataclasses import dataclass, field
from typing import Dict, List

from classes.events.event import T
from classes.events.event_manager import EventManager


@dataclass
class EventRepo(EventManager):
    """Repository for storing events."""

    events: Dict[int, List[T]] = field(default_factory=dict)

    def store_event(self, event: T):
        """Store an event in the repository."""
        if event.id not in self.events:
            self.events[event.id] = []
        self.events[event.id].append(event)
        self.notify(event.name, event)

    def get_events(self, id: int) -> List[T]:
        """Get all events for a partition key, sorted by timestamp."""
        return sorted(self.events.get(id, []), key=lambda e: e.timestamp)
