from dataclasses import dataclass, field
from classes.aggregate.aggregate_base import Aggregate
from classes.events.event import event


@dataclass
class GroupingAggregate(Aggregate):
    size: int
    _articles: set = field(default_factory=set)

    def _validate_position(self, position: int):
        if position < 1 or position > self.size + 1:
            raise ValueError(
                "Invalid position. Position must be greater than 0 and less than or equal to the number of articles in the grouping plus 1"
            )

    def _validate_article_exists(self, article_id: str):
        if article_id not in self._articles:
            raise ValueError(f"Article {article_id} not found in grouping")

    @event("ArticleCreated")
    def add_article_to_grouping(self, article_id: str, position: int):
        pass

    @event("ArticleReordered")
    def reorder_article_in_grouping(self, article_id: str, position: int):
        pass

    @event("ArticleDeleted")
    def delete_article_from_grouping(self, article_id: str, backfill: bool):
        pass

    @event("NumberOfStoriesChanged")
    def set_size(self, size: int):
        self.size = size
