from dataclasses import dataclass, field

from classes.events.event_listener import AbstractListener


@dataclass
class EventManager:
    listeners: list[AbstractListener] = field(default_factory=list)

    def add_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)
            return
        raise ValueError("Listener already exists")

    def remove_listener(self, listener):
        try:
            self.listeners.remove(listener)
        except ValueError as e:
            raise ValueError("Listener not found") from e

    def notify(self, data):
        for listener in self.listeners:
            listener.notify(data)
