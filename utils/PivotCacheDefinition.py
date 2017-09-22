from bs4 import BeautifulSoup


import zipfile


class PivotCacheDefinition:
    def __init__(self, file_name):
        self.file_name = file_name

    def open(self):
        xlsx_file = zipfile.ZipFile(self.file_name)
        cache_names = list(filter(lambda x: 'pivotCacheDefinition' in x, xlsx_file.namelist()))
        if len(cache_names) == 0:
            raise Exception("Could not find any pivotCacheDefinition: It is not a PivotTable excel file")
        return [xlsx_file.open(cache_name) for cache_name in cache_names]

    def read(self):
        return [str(cache_file.read(), "utf-8") for cache_file in self.open()]

    def parse(self):
        xml_file = self.read()[0]
        print(xml_file)
        soup = BeautifulSoup(xml_file, 'xml')
        columns_data = soup.findAll("cacheField")
        return [
            {
                "name": col["name"],
                "levels": [item["v"] if item.name == "s" else int(item["v"]) for item in col.find("sharedItems").findAll()]
            }
            for col in columns_data
        ]
