# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from search_data.items import SearchDataItem

prefectures ={
    "ibaraki": {
        'allowed_domains' : ['www.pref.ibaraki.jp'],
        'start_urls' : ['https://www.pref.ibaraki.jp/kikaku/joho/it/opendata/od-00.html'],
        'rule1' : r'/od-0[0-6].html',
        'rule2' : r'/kikaku/joho/it/opendata/od-0[1-6]/.+',
        'title_css' : 'html > head > title::text',
        'text_css' : 'table'
    }
}


class CrawlDataSpider(CrawlSpider):
    name = 'crawl_data'
    prefecture = 'ibaraki'


    pre_rules = prefectures[prefecture]
    allowed_domains = pre_rules['allowed_domains']
    start_urls = pre_rules['start_urls']

    rules = (
        # 正規表現にマッチするリンクをクローリング
        Rule(LinkExtractor(allow=pre_rules['rule1'])),
        # # 正規表現にマッチするリンクをparseメソッドでスクレイピング
        Rule(LinkExtractor(allow=pre_rules['rule2']), follow=True, callback='parse_item'),
    )

    counter = 0
    def parse_item(self, response):
        item = SearchDataItem()
        item['url'] = response.url
        item['title'] = response.css(self.pre_rules['title_css']).extract()
        data_text = response.css(self.pre_rules['text_css']).xpath('string()').extract()
        item['text'] = " ".join(data_text[0].split())
        return item







# class CrawlDataSpider(CrawlSpider):
#     name = 'crawl_data'

#     allowed_domains = ['www.pref.ibaraki.jp']
#     start_urls = ['https://www.pref.ibaraki.jp/kikaku/joho/it/opendata/od-00.html']
#     rules = (
#         # 正規表現にマッチするリンクをクローリング
#         Rule(LinkExtractor(allow=r'/od-0[0-6].html')),
#         # # 正規表現にマッチするリンクをparseメソッドでスクレイピング
#         # Rule(LinkExtractor(allow=r'/kikaku/joho/it/opendata/od-01/050500_20170120_kaki.+'), follow=True, callback='parse_item'),
#         Rule(LinkExtractor(allow=r'/kikaku/joho/it/opendata/od-0[1-6]/.+'), follow=True, callback='parse_item'),
#     )
#     counter = 0
#     def parse_item(self, response):
#         item = SearchDataItem()
#         item['url'] = response.url
#         item['title'] = response.css('html > head > title::text').extract()
#         data_text = response.css('table').xpath('string()').extract()
#         item['text'] = " ".join(data_text[0].split())
#         return item
