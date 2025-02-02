from dataclasses import dataclass, field
from datetime import datetime
import pprint


from classes.dataclasses.event import (
    T,
    ArticleCreated,
    ArticleDeleted,
    ArticleReordered,
)
from classes.repositories.event_repo import EventRepo


@dataclass(kw_only=True)
class Aggregate:
    id: int
    type: str
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    version: int = 1
    event_store = EventRepo()

    def _add_event(self, event: T):
        self.event_store.store_event(event)
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

    def add_article_to_grouping(self, article_id: str, position: int = 0):
        self.grouping.insert(position, article_id)
        article_created_event = ArticleCreated(self.id, article_id, position)
        self._add_event(article_created_event)

    def reorder_article_in_grouping(self, article_id: str, new_position: int = 0):
        old_position = self._get_index(article_id)
        self.grouping.pop(old_position)

        self.grouping.insert(new_position, article_id)
        article_reorder_event = ArticleReordered(self.id, article_id, new_position)
        self._add_event(article_reorder_event)

    def delete_article_from_grouping(self, article_id: str):
        self._get_index(article_id)
        self.grouping.pop(article_id)
        article_deleted_event = ArticleDeleted(self.id, article_id)
        self._add_event(article_deleted_event)
