from itertools import chain


class ChainedQuerysetsWithCount:
    def __init__(self, *querysets):
        self.chained_queryset = chain(*querysets)
        self.total_count = sum(map(lambda queryset: queryset.count(), querysets))

    def __iter__(self):
        return self.chained_queryset
    
    def count(self):
        return self.total_count

