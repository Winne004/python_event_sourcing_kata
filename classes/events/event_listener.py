from abc import ABC, abstractmethod
from typing import Type


from classes.query_models.baskets import Baskets
from classes.events.event import T


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
        pass


class ArticlesProjector(AbstractListener):
    def notify(self, event_name: str, event: T) -> None:
        pass
