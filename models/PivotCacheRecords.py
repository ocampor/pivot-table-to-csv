from models import PivotCache


class PivotCacheRecords(PivotCache):
    def __init__(self, file_name):
        self.pivot_cache_name = 'pivotCacheRecords'
        self.file_name = file_name
