from classes.dataclasses.aggregate import GroupingAggregate
from classes.dataclasses.event import ArticleCreated
from classes.repositories.event_listener import BasketsProjector


grouping = 12345
basket_instance = BasketsProjector()

grouping_aggregate = GroupingAggregate(id=grouping, type="grouping")
grouping_aggregate.event_store.add_listener(ArticleCreated.__name__, basket_instance)

grouping_aggregate.add_article_to_grouping("A", 1)
grouping_aggregate.add_article_to_grouping("B", 1)
grouping_aggregate.add_article_to_grouping("C", 1)
grouping_aggregate.reorder_article_in_grouping("B", 0)

print(grouping_aggregate.grouping)
