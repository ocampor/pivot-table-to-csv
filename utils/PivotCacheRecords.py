import zipfile


class PivotCacheRecords:
    def __init__(self, file_name):
        self.file_name = file_name

    def open(self):
        xlsx_file = zipfile.ZipFile(self.file_name)
        cache_names = list(filter(lambda x: 'pivotCacheRecords' in x, xlsx_file.namelist()))
        if len(cache_names) == 0:
            raise Exception("Could not find any pivotCacheRecords: It is not a PivotTable excel file")
        return [xlsx_file.open(cache_name) for cache_name in cache_names]

    def read(self):
        return [str(cache_file.read(), "utf-8") for cache_file in self.open()]
