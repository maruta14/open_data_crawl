# -*- coding: utf-8 -*-
import scrapy
import pickle
from scrapy_splash import SplashRequest
from search_data.items import SearchDataItem



tochigi_urls_path = "../../urls/tochigi_urls.pickle"
hyogo_urls_path = "../../urls/hyogo_urls.pickle"
nagano_urls_path = "../../urls/nagano_urls.pickle"
shizuoka_urls_path = "../../urls/shizuoka_urls.pickle"
chiba_urls_path = "../../urls/chiba_urls.pickle"

PREFECTURES_PARAMETER = {
    "tochigi": {
        'allowed_domains' : ['tochigiken.jp'],
        'title_css' : '#mdb_detail_print_20 > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td::text',
        'text_css' : '#mdb_detail_print_20'
    },
    "hyogo": {
        'allowed_domains' : ['open-data.pref.hyogo.lg.jp'],
        'title_css' : 'head > title::text',
        'title_css2' : '#_79 > tbody > tr > td > table > tbody > tr > td > div > div > div#mdb_detail_print_79 > table > tbody > tr > td > table > tbody > tr:nth-child(1)',
        'text_css' : '#_79 > tbody > tr > td > table > tbody > tr > td > div > div'
    },
    "nagano": {
        'allowed_domains' : ['tokei.pref.nagano.lg.jp'],
        'title_css' : 'head > title::text',
        'text_css' : '#main > div.page-contents.border-top02 > section',
    },
    "shizuoka": {
        'allowed_domains' : ['opendata.pref.shizuoka.jp'],
        'title_css' : 'head > title::text',
        'text_css' : '#main > div.contents',
        'text_css2' : '#cms-tab-7-0-view > div > div',
    },
    "chiba": {
        'allowed_domains' : ['opendata.pref.shizuoka.jp'],
        'title_css' : 'head > title::text',
        'text_css' : '#tmp_contents',
        # 'text_css2' : '#cms-tab-7-0-view > div > div',
    },


}


class JavaScriptSpiderSpider(scrapy.Spider):
    name = 'java_script_spider'
    prefecture = 'chiba'
    pre_rules = PREFECTURES_PARAMETER[prefecture]

    allowed_domains = pre_rules['allowed_domains']

    if prefecture == 'tochigi':
        with open(tochigi_urls_path, "rb") as f:
            start_urls = pickle.load(f)
    elif prefecture == 'hyogo':
        with open(hyogo_urls_path, "rb") as f:
            start_urls = pickle.load(f)
    elif prefecture == 'nagano':
        with open(nagano_urls_path, "rb") as f:
            start_urls = pickle.load(f)
    elif prefecture == 'shizuoka':
        with open(shizuoka_urls_path, "rb") as f:
            start_urls = pickle.load(f)
    elif prefecture == 'chiba':
        with open(chiba_urls_path, "rb") as f:
            start_urls = pickle.load(f)
    

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url = url, callback = self.parse, endpoint = "render.html")

    def parse(self, response):
        item = SearchDataItem()
        item['url'] = response.url
        title = response.css(self.pre_rules['title_css']).extract()

        try:
            title.append(response.css(self.pre_rules['title_css2']).xpath('string()').extract()[0])
        except:
            pass
        
        title = " ".join(title)
        item['title'] = [" ".join(title.split())]

        data_text = response.css(self.pre_rules['text_css']).xpath('string()').extract()
        try:
            data_text.append(response.css(self.pre_rules['text_css2']).xpath('string()').extract()[0])
        except:
            pass
        try:
            data_text.append(response.css(self.pre_rules['text_css3']).xpath('string()').extract()[0])
        except:
            pass
        try:
            data_text.append(response.css(self.pre_rules['text_css4']).xpath('string()').extract()[0])
        except:
            pass
                    
        data_text = " ".join(data_text)
        item['text'] = " ".join(data_text.split())
        return item
