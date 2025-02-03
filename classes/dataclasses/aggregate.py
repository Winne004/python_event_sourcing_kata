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
    _size: int = 0
    _articles: set = field(default_factory=set)

    def _validate_position(self, position: int):
        if position < 1 or position > self._size + 1:
            raise ValueError(
                "Invalid position. Position must be greater than 0 and less than or equal to the number of articles in the grouping plus 1"
            )

    def _validate_article_exists(self, article_id: str):
        if article_id not in self._articles:
            raise ValueError(f"Article {article_id} not found in grouping")

    def add_article_to_grouping(self, article_id: str, position: int = 1):
        self._validate_position(position)

        article_created_event = ArticleCreated(self.id, article_id, position)
        self._add_event(article_created_event)

        self._size += 1
        self._articles.add(article_id)

    def reorder_article_in_grouping(self, article_id: str, new_position: int = 1):
        self._validate_position(new_position)
        self._validate_article_exists(article_id)

        article_reorder_event = ArticleReordered(self.id, article_id, new_position)
        self._add_event(article_reorder_event)

    def delete_article_from_grouping(self, article_id: str):
        self._validate_article_exists(article_id)
        article_deleted_event = ArticleDeleted(self.id, article_id)
        self._add_event(article_deleted_event)

        self._articles.remove(article_id)
        self._size -= 1
