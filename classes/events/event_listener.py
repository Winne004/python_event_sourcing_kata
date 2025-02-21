from abc import ABC, abstractmethod

from classes.events.event import T


class AbstractListener(ABC):
    @abstractmethod
    def notify(self, event: T):
        pass


# class BasketsProjector(AbstractListener):
#     def notify(self, event: T):
#         print(f"Projecting basket event {event}")


# class ArticlesProjector(AbstractListener):
#     def notify(self, event: T):
#         print(f"Projecting article event {event}")
