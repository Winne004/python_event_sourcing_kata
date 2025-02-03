from dataclasses import field, dataclass
from datetime import datetime


@dataclass
class Article:
    sort_index: tuple = field(init=False, repr=False)  # Used for sorting
    id: int
    timestamp: datetime
    position: int = 0

    def __post_init__(self):
        # Sorting by id (ascending) first, then by timestamp (descending)
        self.sort_index = (self.position, -self.timestamp.timestamp())
