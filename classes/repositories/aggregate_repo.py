from dataclasses import dataclass, field
from typing import Dict

from classes.aggregate.aggregate_base import A


@dataclass
class AggregateRepo:
    """Repository for storing aggregates."""

    aggregates: Dict[str, A] = field(default_factory=dict)

    def store_aggregate(self, aggregate: A):
        """Store an aggregate in the repository."""
        self.aggregates[aggregate.id] = aggregate

    def get_aggregate(self, aggregate_id: str) -> A:
        """Get an aggregate by its ID."""
        return self.aggregates.get(aggregate_id)
