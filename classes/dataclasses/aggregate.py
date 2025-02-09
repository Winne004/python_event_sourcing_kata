from dataclasses import dataclass, field
from datetime import datetime
import pprint


from classes.dataclasses.event import (
    T,
    event,
)
from classes.repositories.event_repo import EventRepo


@dataclass(kw_only=True)
class Aggregate:
    id: int
    type: str
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    version: int = 1
    event_store = EventRepo()

    def add_event(self, event_instance: T):
        self.event_store.store_event(event_instance)
        return self

    @classmethod
    def load_events(
        self,
        key: str,
    ):
        events = self.event_store.get_events(key)
        return events


@dataclass
class Article(Aggregate):
    id: str
    position: str


@dataclass
class GroupingAggregate(Aggregate):
    grouping: list = field(default_factory=list)

    def __str__(self):
        return pprint.pformat(self.grouping)

    def _get_index(self, article_id: str):
        try:
            return self.grouping.index(article_id)
        except ValueError:
            print(f"Article {article_id} not found in grouping")

    @event("ArticleCreated")
    def add_article_to_grouping(self, article_id: str, position: int = 0):
        pass

    @event("ArticleReordered")
    def reorder_article_in_grouping(self, article_id: str, new_position: int = 0):
        pass

    @event("ArticleDeleted")
    def delete_article_from_grouping(self, article_id: str):
        pass
