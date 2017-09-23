from bs4 import BeautifulSoup

from models import PivotCache


class PivotCacheDefinition(PivotCache):
    def __init__(self, file_name):
        self.pivot_cache_name = 'pivotCacheDefinition'
        self.file_name = file_name

    def parse(self):
        xml = self.read().pop()
        soup = BeautifulSoup(xml, "xml")
        columns_metadata = soup.findAll("cacheField")
        return map(PivotCacheDefinition.parse_column_metadata, columns_metadata)

    @staticmethod
    def parse_column_metadata(column_metadata):
        return {
            "column_name": column_metadata["name"],
            "levels": PivotCacheDefinition.parse_shared_items(column_metadata.find("sharedItems"))
        }

    @staticmethod
    def parse_shared_items(shared_items):
        levels_tags = []
        if shared_items is not None:
            levels_tags = shared_items.findAll()
        return [PivotCacheDefinition._cast_level_tag_value(item.name, item["v"]) for item in levels_tags]

    @staticmethod
    def _cast_level_tag_value(tag, value):
        if tag == "s":
            return str(value)
        elif tag == "n":
            return str(value)
        else:
            raise TypeError("Tag %s is not defined to be cased" % tag)
