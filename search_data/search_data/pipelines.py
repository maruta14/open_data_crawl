# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy.exporter import CsvItemExporter
# from itemadapter import ItemAdapter

class SearchDataPipeline:
    def process_item(self, item, spider):
        
        if len(item["title"]) == 1 and len(item["text"]) > 1:
            return item

