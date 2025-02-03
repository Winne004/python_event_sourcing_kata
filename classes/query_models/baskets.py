from dataclasses import dataclass, field

from classes.query_models.baskets_article import Article
from classes.dataclasses.event import T


def transform_event_to_article(event: T):
    return Article(position=event.position, id=event.id, timestamp=event.timestamp)


@dataclass
class Basket:
    articles: list[Article] = field(default_factory=list)
    size: int = 2

    def _transform(self, event: T):
        return Article(position=event.position, id=event.id, timestamp=event.timestamp)

    def add_article(self, event: T):
        article: Article = self._transform(event)

        if not (1 <= article.position <= len(self.articles) + 1):
            raise ValueError("Invalid position")

        self.articles.append(event)

        self._re_index()

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
