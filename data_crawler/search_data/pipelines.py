# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy.exporter import CsvItemExporter
# from itemadapter import ItemAdapter

import re

class SearchDataPipeline:
    def process_item(self, item, spider):


        if "三重県" in item["title"]:
            if not "Excel" or "EXCEL" or "CSV" in item['text']:
                item["title"] = ""
        if "奈良県" in item["title"]:
            if not "csv" or "xlsx" or "Excel" in item['text']:
                item["title"] = ""
        if "鳥取県" in item["title"]:
            if not "csv" or "xlsx" or "Excel" or "CSV" in item['text']:
                item["title"] = ""
        if "島根県" in item["title"]:
            if not "csv" or " XLSX" or "Excel" or "CSV" in item['text']:
                item["title"] = ""
        if "おかやま" in item["title"][0]:
            if not "XLS" or " XLSX" or "Excel" or "CSV" in item['text']:
                item["title"] = ""
        if "CKAN" in item["title"][0]:
            if "XLS" in item['text'] or " XLSX" in item['text'] or "Excel" in item['text'] or "CSV" in item['text']:
                pass
            else:
                item["title"] = ""
        if "Our Open Data" in item["title"][0]:
            if "XLS" in item['text'] or "xls" in item['text'] or "CSV" in item['text'] or "csv" in item['text']:
                item["text"] = re.sub('//.*]>', '', item["text"])
                item["text"] = re.sub('\(fun.*;$', '', item["text"])
            else:
                item["title"] = ""
        if "愛媛県" in item["title"][0]:
            if "XLS" in item['text'] or "xls" in item['text'] or "CSV" in item['text'] or "csv" in item['text']:
                item["text"] = re.sub('//.*]>', '', item["text"])
            else:
                item["title"] = ""
        if "鹿児島" in item["title"][0]:            
            item["text"] = re.sub('ツイート.*;', '', item["text"])


        if len(item["title"]) == 1 and len(item["text"]) > 1:
            return item
        


