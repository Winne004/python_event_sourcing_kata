from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, TypeVar, Generic

T = TypeVar("T", bound="EventBase")


@dataclass(order=True)
class EventBase(Generic[T]):
    """Base event class that automatically wraps itself in metadata."""

    partition_key: int
    timestamp: datetime = field(
        default_factory=datetime.now, kw_only=True, compare=True
    )
    _counter: ClassVar[int] = 0  # Class-level counter

    def __post_init__(self):
        """Use the event counter as the sort index and derive the name dynamically."""
        type(self)._counter += 1
        self.name = type(self).__name__


@dataclass
class ArticleCreated(EventBase):
    id: str
    position: int = 0


@dataclass
class ArticleReordered(EventBase):
    id: str
    new_position: int = 0


@dataclass
class ArticleDeleted(EventBase):
    id: str
    position: int = 0
