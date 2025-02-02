from dataclasses import dataclass, field


@dataclass
class EventManager:
    listeners: dict = field(default_factory=dict)

    def add_listener(self, event_name, listener):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def remove_listener(self, event_name, listener):
        if event_name in self.listeners:
            self.listeners[event_name].remove(listener)

    def notify(self, event_name, data):
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener.notify(event_name, data)
