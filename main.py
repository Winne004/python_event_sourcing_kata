from classes.dataclasses.aggregate import GroupingAggregate
from classes.query_models.baskets import Baskets
from classes.dataclasses.event import ArticleCreated, ArticleReordered
from classes.events.event_listener import BasketsProjector


grouping = 12345

basket = Baskets()

basket_instance = BasketsProjector(projector=basket)

grouping_aggregate = GroupingAggregate(id=grouping, type="grouping")

grouping_aggregate.event_store.add_listener(ArticleCreated.__name__, basket_instance)
grouping_aggregate.event_store.add_listener(ArticleReordered.__name__, basket_instance)


grouping_aggregate.add_article_to_grouping("A", 1)
grouping_aggregate.add_article_to_grouping("B", 1)
grouping_aggregate.add_article_to_grouping("C", 1)
grouping_aggregate.reorder_article_in_grouping("B", 1)
grouping_aggregate.delete_article_from_grouping("C")


print(basket.baskets[12345])
