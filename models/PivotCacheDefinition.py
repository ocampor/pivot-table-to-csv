from bs4 import BeautifulSoup

from models import PivotCache


class PivotCacheDefinition(PivotCache):
    def __init__(self, file_name):
        self.pivot_cache_name = 'pivotCacheDefinition'
        self.file_name = file_name

    def parse(self):
        xml_file = self.read().pop()
        soup = BeautifulSoup(xml_file, 'xml')
        columns_data = soup.findAll("cacheField")
        return [
            {
                "name": col["name"],
                "levels": [item["v"] if item.name == "s" else int(item["v"]) for item in col.find("sharedItems").findAll()]
            }
            for col in columns_data
        ]
