# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from search_data.items import SearchDataItem


class CrawlDataSpider(CrawlSpider):
    name = 'crawl_data'


    # allowed_domains = ['toyokeizai.net']
    # start_urls = ['https://toyokeizai.net']
    # rules = (
    #     # 正規表現にマッチするリンクをクローリング
    #     # Rule(LinkExtractor(allow=r'/articles/-/409835')),
    #     # # 正規表現にマッチするリンクをparseメソッドでスクレイピング  /articles/-/409835
    #     Rule(LinkExtractor(allow=r'/articles/-/409835'), follow=True, callback='parse_item'),
    # )


    allowed_domains = ['www.pref.ibaraki.jp']
    start_urls = ['https://www.pref.ibaraki.jp/kikaku/joho/it/opendata/od-00.html']
    rules = (
        # 正規表現にマッチするリンクをクローリング
        Rule(LinkExtractor(allow=r'/od-0[0-6].html')),
        # # 正規表現にマッチするリンクをparseメソッドでスクレイピング
        # Rule(LinkExtractor(allow=r'/kikaku/joho/it/opendata/od-01/050500_20170120_kaki.+'), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=r'/kikaku/joho/it/opendata/od-0[1-6]/.+'), follow=True, callback='parse_item'),
    )
    counter = 0
    def parse_item(self, response):
        item = SearchDataItem()
        item['url'] = response.url
        item['title'] = response.css('html > head > title::text').extract()
        data_text = response.css('table').xpath('string()').extract()
        item['text'] = " ".join(data_text[0].split())
        return item
