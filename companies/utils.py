class ChainWithCount:
    def __init__(self, chained_queryset, total_count):
        self.chained_queryset = chained_queryset
        self.total_count = total_count

    def __iter__(self):
        return self.chained_queryset
    
    def count(self):
        return self.total_count

