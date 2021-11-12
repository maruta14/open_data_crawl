# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from scrapy.exporter import CsvItemExporter

class SearchDataPipeline:
    def process_item(self, item, spider):
        return item

# class PerYearCsvExportPipeline:
#     """Distribute items across multiple XML files according to their 'year' field"""

#     def open_spider(self, spider):
#         self.year_to_exporter = {}

#     def close_spider(self, spider):
#         for exporter, xml_file in self.year_to_exporter.values():
#             exporter.finish_exporting()
#             xml_file.close()

#     def _exporter_for_item(self, item):
#         adapter = ItemAdapter(item)
#         year = adapter['year']
#         if year not in self.year_to_exporter:
#             xml_file = open(f'{year}.csv', 'wb')
#             exporter = CsvItemExporter(xml_file)
#             exporter.start_exporting()
#             self.year_to_exporter[year] = (exporter, xml_file)
#         return self.year_to_exporter[year][0]

#     def process_item(self, item, spider):
#         exporter = self._exporter_for_item(item)
#         exporter.export_item(item)
#         return item

# from scrapy.exceptions import DropItem

# class DuplicatesPipeline(object):

#     def __init__(self):
#         self.ids_seen = set()

#     def process_item(self, item, spider):
#         if item['id'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['id'])
#             return item
