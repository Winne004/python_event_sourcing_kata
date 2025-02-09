from classes.aggregate.aggregate_base import GroupingAggregate


grouping = 12345

# basket_instance = BasketsProjector(projector=basket)

grouping_aggregate = GroupingAggregate(id=grouping, type="grouping")

grouping_aggregate.add_article_to_grouping("A", 1)
grouping_aggregate.add_article_to_grouping("B", 1)
grouping_aggregate.add_article_to_grouping("C", 1)
grouping_aggregate.reorder_article_in_grouping("B", 1)
grouping_aggregate.delete_article_from_grouping("C")


test = grouping_aggregate.event_store.get_events(grouping)
pass
