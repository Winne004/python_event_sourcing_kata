from abc import ABC, abstractmethod


from classes.query_models.baskets import Baskets
from classes.dataclasses.event import T, ArticleCreated


class AbstractListener(ABC):
    @abstractmethod
    def notify(self, event_name: str, event: T) -> None:
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

    def notify(self, event_name: str, event: T) -> None:
        if event_name == ArticleCreated.__name__:
            print("Projecting basket create event")
            self.projector.add_article_to_basket(event.partition_key, event)

        print(f"Projecting basket event: {event}")


class ArticlesProjector(AbstractListener):
    def notify(self, event_name: str, event: T) -> None:
        print(f"Projecting article event: {event}")
