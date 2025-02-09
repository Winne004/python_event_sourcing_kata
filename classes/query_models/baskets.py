from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic, Type

from classes.query_models.baskets_article import Article
from classes.dataclasses.event import T, ArticleCreated, ArticleReordered


def transform_event_to_article(event: Type[T]):
    return Article(position=event.position, id=event.id, timestamp=event.timestamp)


@dataclass
class Basket:
    articles: list[Article] = field(default_factory=list)
    size: int = 2

    def _transform(self, event: Type[T]):
        return Article(position=event.position, id=event.id, timestamp=event.timestamp)

    def add_article(self, event: ArticleCreated):
        article: Article = self._transform(event)

        if not (1 <= article.position <= len(self.articles) + 1):
            raise ValueError("Invalid position")

        self.articles.append(article)

        self._re_index()

    def reorder_article(self, event: ArticleReordered):
        article: Article = self._transform(event)
        for i, _article in enumerate(self.articles):
            if _article.id == article.id:
                self.articles[i] = article
                self._re_index()
                return

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

    def _re_index(self, backfill=False):
        self._sort()
        self._recalculate_positions(backfill)


@dataclass
class Baskets:
    baskets: dict[int, Basket] = field(default_factory=dict)

    def add_article_to_basket(self, basket_id, event):
        basket = self.baskets.get(basket_id, None)

        if not basket:
            self.baskets[basket_id] = Basket()

        basket = self.baskets[basket_id]

        basket.add_article(event)

    def reorder_article_in_basket(self, basket_id, event):
        basket = self.baskets.get(basket_id, None)

        if not basket:
            raise ValueError("Basket not found")

        basket.reorder_article(event)
