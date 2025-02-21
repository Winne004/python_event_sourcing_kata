from classes.aggregate.grouping_aggregate import GroupingAggregate
from classes.query_models.baskets import Baskets
from classes.repositories.event_repo import EventRepo


grouping = 12345

event_store = EventRepo()

projection = Baskets()

event_store.add_listener(projection)

# grouping_aggregate = GroupingAggregate(
#     id=grouping, type="grouping", version=1, size=3, _event_store=event_store
# )
grouping_aggregate = GroupingAggregate(
    aggregate_id=54321, type="grouping", version=1, size=3, _event_store=event_store
)
grouping_aggregate.add_article_to_grouping("A", 0)
grouping_aggregate.add_article_to_grouping("B", 0)
grouping_aggregate.add_article_to_grouping("C", 0)
grouping_aggregate.add_article_to_grouping("D", 3)
grouping_aggregate.reorder_article_in_grouping("B", 0)
grouping_aggregate.delete_article_from_grouping("C", True)
grouping_aggregate.set_size(2)

test = grouping_aggregate.load_events(54321, event_store)
test2 = projection.baskets[54321]
pass
