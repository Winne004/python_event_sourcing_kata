from dataclasses import dataclass, field
from typing import Dict, Generic

from classes.events.event_listener import AbstractListener
from classes.query_models.baskets_article import Article
from classes.events.event import T


def transform_event_to_article(event: T):
    return Article(
        position=event.position, id=event.aggregate_id, timestamp=event.timestamp
    )


@dataclass
class Basket:
    articles: list[Article] = field(default_factory=list)
    size: int = 2

    def _transform(self, event: T):
        return Article(
            position=event.position, id=event.article_id, timestamp=event.timestamp
        )

    def add_article(self, event: T):
        article: Article = self._transform(event)

        if article.id in [article.id for article in self.articles]:
            raise ValueError("Article already exists")

        article.position += 1  # 1-indexed

        if not (1 <= article.position <= len(self.articles) + 1):
            raise ValueError("Invalid position")

        self.articles.append(article)

        self._re_index()

    def reorder_article(self, event: T):
        article: Article = self._transform(event)
        for i, _article in enumerate(self.articles):
            if _article.id == article.id:
                self.articles[i] = article
                self._re_index()
                return

    def delete_article(self, event: T):
        delete_event = event.article_id
        self.articles = [
            article for article in self.articles if article.id != delete_event
        ]
        self._re_index(event.backfill)

    def set_size(self, event: T):
        self.size = event.size
        self._re_index(backfill=True)

    def _recalculate_positions(self, backfill):
        if not backfill:
            for i, article in enumerate(self.articles, 1):
                if article.position == 999:
                    return
                article.position = i

        for i, article in enumerate(self.articles, 1):
            article.position = i if i <= self.size else 999

    def _sort(
        self,
    ):
        self.articles.sort()

    def _re_index(self, backfill=True):
        self._sort()
        self._recalculate_positions(backfill)


@dataclass
class Baskets(AbstractListener):
    baskets: Dict[int, Basket] = field(default_factory=dict)

    def notify(self, event: T) -> None:
        """
        Handles incoming events by creating a basket when needed
        and dispatching events to the correct Basket method.
        """
        missing_attrs = [
            attr for attr in ("name", "aggregate_id") if not hasattr(event, attr)
        ]
        if missing_attrs:
            raise ValueError(f"Invalid event. Missing attributes: {missing_attrs}")

        if event.name == "AggregateCreated" and event.type == "grouping":
            self.baskets[event.aggregate_id] = Basket(size=event.size)
            return

        basket = self.baskets.get(event.aggregate_id)
        if basket is None:
            raise KeyError(f"Basket with id {event.aggregate_id} not found.")

        handlers = {
            "ArticleCreated": basket.add_article,
            "ArticleReordered": basket.reorder_article,
            "ArticleDeleted": basket.delete_article,
            "NumberOfStoriesChanged": basket.set_size,
        }

        handler = handlers.get(event.name)
        if handler:
            handler(event)
