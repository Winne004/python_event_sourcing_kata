from abc import ABC, abstractmethod
from typing import Type


from classes.query_models.baskets import Baskets
from classes.dataclasses.event import T, ArticleCreated, ArticleReordered


class AbstractListener(ABC):
    @abstractmethod
    def notify(self, event_name: str, event: Type[T]) -> None:
        """Handle incoming events."""
        pass


class BasketsProjector(AbstractListener):
    def __init__(self, projector: Baskets):
        """
        Dependency injection for the projector.

        :param projector: Instance of BasketItem (or a mock for testing).
        """
        super().__init__()
        self.projector = projector

    def notify(self, event_name: str, event: Type[T]) -> None:
        mapping = {
            ArticleCreated.__name__: self.projector.add_article_to_basket,
            ArticleReordered.__name__: self.projector.reorder_article_in_basket,
        }

        mapping[event_name](event.partition_key, event)

        print(f"Projecting basket event: {event}")


class ArticlesProjector(AbstractListener):
    def notify(self, event_name: str, event: Type[T]) -> None:
        print(f"Projecting article event: {event}")
