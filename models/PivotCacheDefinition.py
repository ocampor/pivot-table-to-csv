from bs4 import BeautifulSoup

from models import PivotCache
from utils import cast_tag_value


class PivotCacheDefinition(PivotCache):
    def __init__(self, file_name):
        self.pivot_cache_name = 'pivotCacheDefinition'
        self.file_name = file_name

    def parse(self):
        xmls = self.read()
        soups = [BeautifulSoup(xml, "xml") for xml in xmls]
        columns_metadatas = [soup.findAll("cacheField") for soup in soups]
        return [map(PivotCacheDefinition.parse_column_metadata, columns_metadata)
                for columns_metadata in columns_metadatas]

    @staticmethod
    def parse_column_metadata(column_metadata):
        levels = PivotCacheDefinition.parse_shared_items(column_metadata.find("sharedItems"))
        return {
            "column_name": column_metadata["name"],
            "is_categorical": len(levels) > 0,
            "levels": levels
        }

    @staticmethod
    def parse_shared_items(shared_items):
        levels_tags = []
        if shared_items is not None:
            levels_tags = shared_items.findAll()
        return [cast_tag_value(item.name, item["v"]) for item in levels_tags]
