from classes.aggregate.grouping_aggregate import GroupingAggregate
from classes.events.event_listener import BasketsProjector
from classes.repositories.event_repo import EventRepo


grouping = 12345

event_store = EventRepo()

event_store.add_listener(BasketsProjector())

grouping_aggregate = GroupingAggregate(
    id=grouping, type="grouping", version=1, size=3, _event_store=event_store
)
grouping_aggregate = GroupingAggregate(
    id=54321, type="grouping", version=1, size=3, _event_store=event_store
)
grouping_aggregate.add_article_to_grouping("A", 1)
grouping_aggregate.add_article_to_grouping("B")
grouping_aggregate.add_article_to_grouping("C", 1)
grouping_aggregate.reorder_article_in_grouping("B", 1)
grouping_aggregate.delete_article_from_grouping("C")
grouping_aggregate.set_size(2)

test = grouping_aggregate.load_events(54321, event_store)
pass
