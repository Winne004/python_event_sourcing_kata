from dataclasses import dataclass, field
from datetime import datetime
import inspect
from typing import TypeVar, Generic

T = TypeVar("T", bound="EventBase")


@dataclass(order=True)
class EventBase(Generic[T]):
    """Base event class that automatically wraps itself in metadata."""

    partition_key: int
    timestamp: datetime = field(
        default_factory=datetime.now, kw_only=True, compare=True
    )

    def __post_init__(self):
        """Use the event counter as the sort index and derive the name dynamically."""
        self.name = type(self).__name__


def event(name: str):
    """Decorator to dynamically create an event subclass and use it in a method."""

    def decorator(func):
        def wrapper(self, *args):
            signature = inspect.signature(func)
            param_names = [
                name for name in signature.parameters.keys() if name != "self"
            ]

            arg_values = {k: v for k, v in zip(param_names, args)}

            EventClass = type(name, (EventBase,), arg_values)

            event_instance = EventClass(partition_key=self.id)

            print(f"Event {name} was created dynamically")

            func(self, event_instance)

            return self.add_event(event_instance)

        return wrapper

    return decorator
