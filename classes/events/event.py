from dataclasses import dataclass, field, make_dataclass
from datetime import datetime
from functools import wraps
import inspect
from typing import TypeVar, Generic


T = TypeVar("T", bound="EventBase")


@dataclass(order=True)
class EventBase(Generic[T]):
    """Base event class that automatically wraps itself in metadata."""

    id: int
    timestamp: datetime = field(default_factory=datetime.now, compare=True)

    def __post_init__(self):
        """Use the event counter as the sort index and derive the name dynamically."""
        self.name = type(self).__name__


events = {}


def event(name: str):
    """Decorator to dynamically create an event subclass and use it in a method."""

    def decorator(func):
        @wraps(func)  # Preserve original function metadata
        def wrapper(self, *args, **kwargs):
            # Extract event data
            if not getattr(
                self, "initialized", False
            ):  # Avoid AttributeError if `initialized` is missing
                # Capture instance attributes (excluding private/protected ones)
                arg_values = {
                    k: v for k, v in self.__dict__.items() if not k.startswith("_")
                }
            else:
                # Capture function arguments using its signature
                signature = inspect.signature(func)
                param_names = [
                    name for name in signature.parameters.keys() if name != "self"
                ]

                # Merge positional and keyword arguments
                arg_values = {k: v for k, v in zip(param_names, args)}
                arg_values.update(kwargs)

                # Ensure `id` is included
                arg_values["id"] = self.id

            # arg_values["timestamp"] = datetime.now()

            # Create event class only if it doesn't already exist
            if name not in events:
                event_fields = [
                    (
                        k,
                        type(v),
                        field(default=v),
                        # if k != "timestamp"
                        # else field(default_factory=datetime.now),
                    )
                    for k, v in arg_values.items()
                ]
                events[name] = make_dataclass(
                    cls_name=name, fields=event_fields, bases=(EventBase,)
                )

            # Instantiate the event
            event_cls = events[name]
            event_instance = event_cls(**arg_values)

            print(
                f"🔹 Event '{events[name]}' created dynamically with data: {arg_values}"
            )

            # Execute the decorated function
            result = func(self, *args, **kwargs)

            # Add the event to the aggregate
            return self.add_event(event_instance)

        return wrapper

    return decorator
