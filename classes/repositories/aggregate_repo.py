from dataclasses import dataclass, field
from typing import Dict

from classes.dataclasses.aggregate import Aggregate


@dataclass
class AggregateRepo:
    """Repository for storing aggregates."""

    aggregates: Dict[str, Aggregate] = field(default_factory=dict)

    def store_aggregate(self, aggregate: Aggregate):
        """Store an aggregate in the repository."""
        self.aggregates[aggregate.id] = aggregate

    def get_aggregate(self, aggregate_id: str) -> Aggregate:
        """Get an aggregate by its ID."""
        return self.aggregates.get(aggregate_id)
