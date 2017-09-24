import zipfile


class PivotCache:
    _pivot_cache_name = None
    _file_name = None

    def open(self):
        xlsx_file = zipfile.ZipFile(self.file_name)
        cache_names = list(filter(lambda x: self.pivot_cache_name in x and x[-3:] == "xml", xlsx_file.namelist()))
        cache_names = sorted(cache_names)
        if len(cache_names) == 0:
            error_message = "Could not find any {0}: It is not a PivotTable excel file"
            raise Exception(error_message.format(self.pivot_cache_name))
        return [xlsx_file.open(cache_name) for cache_name in cache_names]

    def read(self):
        return [str(cache_file.read(), "utf-8") for cache_file in self.open()]

    @property
    def pivot_cache_name(self):
        if self._pivot_cache_name is None:
            raise NotImplementedError
        else:
            return self._pivot_cache_name

    @pivot_cache_name.setter
    def pivot_cache_name(self, value):
        self._pivot_cache_name = value

    @property
    def file_name(self):
        if self._file_name is None:
            raise NotImplementedError
        else:
            return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value
