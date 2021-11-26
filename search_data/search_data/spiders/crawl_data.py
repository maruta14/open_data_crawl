# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from search_data.items import SearchDataItem
import pickle


tochigi_urls_path = "../../../urls/tochigi_urls.pickle"
prefectures ={
    "ibaraki": {
        'allowed_domains' : ['www.pref.ibaraki.jp'],
        'start_urls' : ['https://www.pref.ibaraki.jp/kikaku/joho/it/opendata/od-00.html'],
        'rule1' : r'/od-0[0-6].html',
        'rule2' : r'/kikaku/joho/it/opendata/od-0[1-6]/.+',
        'title_css' : 'html > head > title::text',
        'text_css' : 'table'
    },
    "hokkaido": {
        'allowed_domains' : ['www.harp.lg.jp'],
        'start_urls' : ['https://www.harp.lg.jp/opendata/dataset/search/index.p5.html', 'https://www.harp.lg.jp/opendata/dataset/search/index.p14.html', 'https://www.harp.lg.jp/opendata/dataset/search/index.p23.html',
                        'https://www.harp.lg.jp/opendata/dataset/search/index.p32.html', 'https://www.harp.lg.jp/opendata/dataset/search/index.p41.html', 'https://www.harp.lg.jp/opendata/dataset/search/index.p50.html', 
                        'https://www.harp.lg.jp/opendata/dataset/search/index.p59.html'],
        'rule1' : r'/index(.p[0-9]*)*\.html',
        'rule2' : r'/[0-9]+\.html',
        'title_css' : 'html > head > title::text',
        'text_css' : 'div#main > div.text',
        'text_css2' : 'div#main > div.dataset-tabs'
    },
    "aomori": {
        'allowed_domains' : ['opendata.pref.aomori.lg.jp'],
        'start_urls' : ['https://opendata.pref.aomori.lg.jp/dataset/search/index.p6.html', 'https://opendata.pref.aomori.lg.jp/dataset/search/index.p15.html', 'https://opendata.pref.aomori.lg.jp/dataset/search/index.p24.html',
                        'https://opendata.pref.aomori.lg.jp/dataset/search/index.p33.html', 'https://opendata.pref.aomori.lg.jp/dataset/search/index.p42.html', 'https://opendata.pref.aomori.lg.jp/dataset/search/index.p51.html',
                        'https://opendata.pref.aomori.lg.jp/dataset/search/index.p60.html'],
        'rule1' : r'/dataset/search/index(.p[0-9]*)*\.html',
        'rule2' : r'/dataset/(dataland-|aoi-mori-)*[0-9]+\.html',
        'title_css' : 'html > head > title::text',
        'text_css' : 'div#main > div.contents',
        'text_css2' : 'div#main > div.dataset-tabs'
    },
    "iwate": {
        'allowed_domains' : ['www.pref.iwate.jp'],
        'start_urls' : ['https://www.pref.iwate.jp/kensei/seisaku/jouhouka/1012070/index.html'],
        # 'rule1' : r'/index(.p[0-9]*)*\.html',
        'rule2' : r'/[0-9]{7}.html',
        'title_css' : 'html > head > title::text',
        'text_css' : 'article#content',
    },
    "miyagi": {
        'allowed_domains' : ['www.pref.miyagi.jp'],
        'start_urls' : ['https://www.pref.miyagi.jp/site/opendata-miyagi/chiiki.html', 'https://www.pref.miyagi.jp/site/opendata-miyagi/gyousei.html', 'https://www.pref.miyagi.jp/site/opendata-miyagi/shinsai.html',
                        'https://www.pref.miyagi.jp/site/opendata-miyagi/kankyou.html', 'https://www.pref.miyagi.jp/site/opendata-miyagi/hoken.html', 'https://www.pref.miyagi.jp/site/opendata-miyagi/keizai.html',
                        'https://www.pref.miyagi.jp/site/opendata-miyagi/nougyou.html', 'https://www.pref.miyagi.jp/site/opendata-miyagi/doboku.html', 'https://www.pref.miyagi.jp/site/opendata-miyagi/bousai.html',
                        'https://www.pref.miyagi.jp/site/opendata-miyagi/kyouiku.html', 'https://www.pref.miyagi.jp/site/opendata-miyagi/covid-19.html'],
        'restrict_css': 'table > tbody > tr > td:nth-child(2) > a',
        'title_css' : 'html > head > title::text',
        'text_css' : 'div.detail_free',
    },
    "akita": {
        'allowed_domains' : ['www.pref.akita.lg.jp'],
        'start_urls' : ['https://www.pref.akita.lg.jp/pages/archive/32419'],
        'restrict_css' : 'main > article > div > div.p-page-body > ul',
        'restrict_css2' : 'main > article > div > div.p-page-body > table',
        'title_css' : 'html > head > title::text',
        'text_css' : '#top > div.l-site-container > main > article > div',
    },
    "yamagata": {
        'allowed_domains' : ['www.pref.yamagata.jp'],
        'start_urls' : ['https://www.pref.yamagata.jp/020051/kensei/shoukai/toukeijouhou/tokeijoho-opendate/opendata/index.html'],
        'restrict_css' : 'div.col2L',
    },
    "hukushima": {
        'allowed_domains' : ['www.pref.fukushima.lg.jp'],
        'start_urls' : ['https://www.pref.fukushima.lg.jp/sec/11045a/open-data-kosodate.html'],
        'restrict_css' : '#main_body > div.detail_free > p:nth-child(1)'
    },
    "tochigi": {
        'allowed_domains' : ['tochigiken.jp'],
        'start_urls' : ['http://tochigiken.jp/?page_id=18'],
        'title_css' : 'div#mdb_detail_print_20 > table > tr:nth-child(1) > td > table > tr:nth-child(1) > td::text',
        'text_css' : '#mdb_detail_print_20 > table'
    },
    "gunma": {
        'allowed_domains' : ['www.pref.gunma.jp'],
        'start_urls' : ['https://www.pref.gunma.jp/07/b2700058.html#tiri1'],
        'restrict_css' : 'div#scroll-main > article > div',
        #scroll-main > article > div:nth-child(11) > table
        'deny_rule' : r"/.+\.(csv|shp|shx|dbf|xls|prj|sbx|xml|sbn)",
        'title_css' : 'head > title::text',
        'text_css' : 'body'
    },
    "saitama": {
        'allowed_domains' : ['opendata.pref.saitama.lg.jp'],
        'start_urls' : ['https://opendata.pref.saitama.lg.jp/data/dataset?page=4', 'https://opendata.pref.saitama.lg.jp/data/dataset?page=7', 'https://opendata.pref.saitama.lg.jp/data/dataset?page=12',
                        'https://opendata.pref.saitama.lg.jp/data/dataset?page=15', 'https://opendata.pref.saitama.lg.jp/data/dataset?page=20', 'https://opendata.pref.saitama.lg.jp/data/dataset?page=25',
                        'https://opendata.pref.saitama.lg.jp/data/dataset?page=30', 'https://opendata.pref.saitama.lg.jp/data/dataset?page=33'],
        'rule1' : r'/data/dataset.page=[0-9]+',
        'rule2' : r'/data/dataset/.*',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",    
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div',
        "depth_limit" : 1     
    },
    "chiba": {
        'allowed_domains' : ['www.pref.chiba.lg.jp'],
        'start_urls' : ['https://www.pref.chiba.lg.jp/kenshidou/opendata/opendata-jinkoudoutai-h30-gaikyou.html'],
        'restrict_css' : '#tmp_rcnt',
        # 'rule2' : r'/opendata-.*\.html',
        'title_css' : 'head > title::text',
        'text_css' : 'div#tmp_contents',
        "depth_limit" : 2
    },
    "tokyo": {
        'allowed_domains' : ['catalog.data.metro.tokyo.lg.jp'],
        'start_urls' : ['https://catalog.data.metro.tokyo.lg.jp/dataset?page=4', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=7', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=12',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=15', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=20', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=25',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=30', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=35', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=40',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=45', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=50', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=55',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=60', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=65', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=70',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=75', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=80', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=85',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=90', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=95', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=100',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=105', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=110', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=115',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=125', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=130', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=135',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=140', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=145', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=150',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=155', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=160', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=165',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=170', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=175', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=180',
                        'https://catalog.data.metro.tokyo.lg.jp/dataset?page=185', 'https://catalog.data.metro.tokyo.lg.jp/dataset?page=190'                        
                        ],
        'rule1' : r'/dataset.page=[0-9]+',
        'rule2' : r'/dataset/.*',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",    
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div',
        "depth_limit" : 2      
    },
    "kanagawa": {
        'allowed_domains' : ['www.pref.kanagawa.jp'],
        'start_urls' : ['https://www.pref.kanagawa.jp/dst/list-1.html', 'https://www.pref.kanagawa.jp/dst/list-2.html', 'https://www.pref.kanagawa.jp/dst/list-3.html'
                        'https://www.pref.kanagawa.jp/dst/list-4.html', 'https://www.pref.kanagawa.jp/dst/list-5.html', 'https://www.pref.kanagawa.jp/dst/list-6.html'],
        'restrict_css' : r'#main_body',
        'title_css' : 'head > title::text',
        'text_css' : '#tmp_contents',
        "depth_limit" : 1
    },
    "niigata": {
        'allowed_domains' : ['www.pref.niigata.lg.jp'],
        'start_urls' : ['https://www.pref.niigata.lg.jp/site/opendata/list1442-3889.html'],
        'restrict_css' : r'#subsite_menu_wrap',
        'restrict_css2' : r'#main_body',
        'title_css' : 'head > title::text',
        'text_css' : '#main_body > div.detail_free',
        "depth_limit" : 2
    },
    "toyama": {
        'allowed_domains' : ['opendata.pref.toyama.jp'],
        'start_urls' : ['https://opendata.pref.toyama.jp/dataset?page=4', 'https://opendata.pref.toyama.jp/dataset?page=9', 'https://opendata.pref.toyama.jp/dataset?page=14',
                        'https://opendata.pref.toyama.jp/dataset?page=19', 'https://opendata.pref.toyama.jp/dataset?page=24', 'https://opendata.pref.toyama.jp/dataset?page=29', 
                        'https://opendata.pref.toyama.jp/dataset?page=34', 'https://opendata.pref.toyama.jp/dataset?page=39', 'https://opendata.pref.toyama.jp/dataset?page=44',
                        'https://opendata.pref.toyama.jp/dataset?page=49', 'https://opendata.pref.toyama.jp/dataset?page=54','https://opendata.pref.toyama.jp/dataset?page=57'],
        'rule1' : r'/dataset.page=[0-9]+',
        'rule2' : r'/dataset/.*',
        'deny_rule' : r"/dataset/.*/resource/.*",    
        'title_css' : 'head > title::text',
        'text_css' : 'body > section > div > div > div',
        "depth_limit" : 2      
    },
    "ishikawa": {
        'allowed_domains' : ['www.pref.ishikawa.lg.jp'],
        'start_urls' : ['https://www.pref.ishikawa.lg.jp/opendata/index.html'],
        'restrict_css' : r'#tmp_contents > ul:nth-child(16)',
        "depth_limit" : 2
    },
    "hukui": {
        'allowed_domains' : ['www.pref.fukui.lg.jp'],
        'start_urls' : ['https://www.pref.fukui.lg.jp/doc/toukei-jouhou/opendata/category.html'],
        'rule1' : r'/doc/toukei-jouhou/opendata/list_[0-9]+\.html',
        'title_css' : '#tmp_contents > table > tbody > tr > td:nth-child(1)',
        'text_css' : '#tmp_contents > table > tbody > tr',
        "depth_limit" : 2
    },
    "yamanashi": {
        'allowed_domains' : ['www.pref.yamanashi.jp'],
        'start_urls' : ['https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=5_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=15_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=25_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=35_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=45_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=55_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=65_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=75_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=85_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=95_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=105_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=115_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        'https://www.pref.yamanashi.jp/opendata/catalog/index.php?p=120_p&asc=data_link_title&displayedresults=100#tmp_opdata_result',
                        ],
        'rule1' : r'\?p=[0-9]+_[a-z]&asc=data_link_title&displayedresults=100#tmp_opdata_result',
        'restrict_css' : '#tmp_opdata_result > table',
        'title_css' : 'head > title::text',
        'text_css' : 'div#tmp_contents',
        "depth_limit" : 2
    },
    "nagano": {
        'allowed_domains' : ['tokei.pref.nagano.lg.jp'],
        'start_urls' : ['https://tokei.pref.nagano.lg.jp/statistics-info/search-field'],
        'rule1' : r'/statistics_field/statistics_field[0-9]+',
        'rule2' : r'/[0-9]+\.html',
        'rule3' : r'/statistics/[0-9]+\.html',
        'restrict_css' : '#search-item-list-box',
        'title_css' : 'head > title::text',
        'text_css' : '#main > div.page-contents.border-top02 > section',
        "depth_limit" : 3
    },
    "gifu": {
        'allowed_domains' : ['gifu-opendata.pref.gifu.lg.jp'],
        'start_urls' : ['https://gifu-opendata.pref.gifu.lg.jp/dataset?page=4', 'https://gifu-opendata.pref.gifu.lg.jp/dataset?page=9', 'https://gifu-opendata.pref.gifu.lg.jp/dataset?page=14',
                        'https://gifu-opendata.pref.gifu.lg.jp/dataset?page=19', 'https://gifu-opendata.pref.gifu.lg.jp/dataset?page=24', 'https://gifu-opendata.pref.gifu.lg.jp/dataset?page=28'],
        'rule1' : r'/dataset.page=[0-9]+',
        'rule2' : r'/dataset/.*',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",    
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2   
    },
    "sizuoka": {
        'allowed_domains' : ['opendata.pref.shizuoka.jp'],
        'start_urls' : ['https://opendata.pref.shizuoka.jp/dataset/search?page=5',],
        'rule1' : r'/dataset/search.page=[0-9]+',
        'rule2' : r'/dataset/.*\.html',
        # 'deny_rule' : r"/dataset/.*(resource|groups|activity).*",    
        'title_css' : 'head > title::text',
        'text_css' : '#main > div.contents',
        'text_css2' : '#cms-tab-7-0-view > div > div > dl',
        "depth_limit" : 2   
    },
    "aichi": {
        'allowed_domains' : ['www.pref.aichi.jp'],
        'start_urls' : ['https://www.pref.aichi.jp/life/6/34/114/'],
        'restrict_css' : '#life1_news',
        'title_css' : 'head > title::text',
        'text_css' : '#main_body > div.detail_free',
        "depth_limit" : 2   
    },
    "mie": {
        'allowed_domains' : ['www.pref.aichi.jp'],
        'start_urls' : ['https://www.pref.mie.lg.jp/IT/HP/87585000001.htm'],
        # 'rule' : r'/IT/HP/[0-9]+\.htm',
        # 'restrict_css' : '#center-contents > div.center-body.clearfix',
        # 'restrict_css2' : '#section1',
        'title_css' : 'head > title::text',
        'text_css' : 'div#section',
        "depth_limit" : 2   
    },

}


class CrawlDataSpider(CrawlSpider):
    name = 'crawl_data'
    prefecture = 'mie'
    pre_rules = prefectures[prefecture]


    allowed_domains = pre_rules['allowed_domains']

    if prefecture == 'tochigi':
        with open(tochigi_urls_path, "rb") as f:
            start_urls = pickle.load(f)
    else:
        start_urls = pre_rules['start_urls']

    # rules = (
    #     # 正規表現にマッチするリンクをクローリング
    #     # Rule(LinkExtractor(restrict_css=pre_rules['restrict_css'])),
    #     # # # 正規表現にマッチするリンクをparseメソッドでスクレイピング
    #     Rule(LinkExtractor(restrict_css=pre_rules['restrict_css2']), follow=True, callback='parse_item'),
    #     # Rule(LinkExtractor(restrict_css=pre_rules['restrict_css']), follow=True, callback='parse_item')
    # )
        

    def parse_item(self, response):
        item = SearchDataItem()
        item['url'] = response.url
        item['title'] = response.css(self.pre_rules['title_css']).extract()
        data_text = response.css(self.pre_rules['text_css']).xpath('string()').extract()

        try:
            data_text.append(response.css(self.pre_rules['text_css2']).xpath('string()').extract()[0])
        except:
            pass
        
        data_text = " ".join(data_text)
        item['text'] = " ".join(data_text.split())
        print(item['title'], item['text'])
        return item


    def parse_aichi(self, response):
        item = SearchDataItem()
        for quote in response.css("#main_body > div.detail_free > div.mol_tableblock > table > tbody > tr"):
            # for post in quote.css("tbody > tr"):
                
            title = quote.css("td:nth-child(1)").xpath('string()').extract()
            if len(title) == 0:
                continue
            item['url'] = response.url
            title = " ".join(title)
            item['title'] = " ".join(title.split())

            data_text = quote.xpath('string()').extract()                
            data_text = " ".join(data_text)
            item['text'] = " ".join(data_text.split())
            print(item['url'], item['title'], item['text'])
            yield item


    def parse_hukui(self, response):
        item = SearchDataItem()
        for quote in response.css("#content > div > div.article > table > tbody > tr"):
            # for post in quote.css("tbody > tr"):
                
            title = quote.css("td:nth-child(1)").xpath('string()').extract()
            if len(title) == 0:
                continue
            item['url'] = response.url
            title = " ".join(title)
            item['title'] = " ".join(title.split())

            data_text = quote.xpath('string()').extract()                
            data_text = " ".join(data_text)
            item['text'] = " ".join(data_text.split())
            print(item['url'], item['title'], item['text'])
            yield item


    def parse_ishikawa(self, response):
        item = SearchDataItem()
        for quote in response.css("#tmp_contents > table > tbody > tr"):
            # for post in quote.css("tbody > tr"):
                
            title = quote.css("td:nth-child(1)").xpath('string()').extract()
            if len(title) == 0:
                continue
            item['url'] = response.url
            title = " ".join(title)
            item['title'] = " ".join(title.split())

            data_text = quote.xpath('string()').extract()                
            data_text = " ".join(data_text)
            item['text'] = " ".join(data_text.split())
            print(item['url'], item['title'], item['text'])
            yield item



    def parse_hukushima(self, response):
        item = SearchDataItem()
        for quote in response.css("#main_body > div.detail_free > table"):
            for post in quote.css("tbody > tr"):
                
                title = post.css("td:nth-child(2)").xpath('string()').extract()
                if len(title) == 0:
                    continue
                item['url'] = response.url
                title = " ".join(title)
                item['title'] = " ".join(title.split())

                data_text = post.xpath('string()').extract()                
                data_text = " ".join(data_text)
                item['text'] = " ".join(data_text.split())
                yield item





    def parse_yamagata(self, response):
        item = SearchDataItem()
        for quote in response.css("div#tmp_contents > table"):
            for post in quote.css("tbody > tr"):
                
                title = post.css("td:nth-child(2)").xpath('string()').extract()
                if len(title) == 0:
                    continue
                item['url'] = response.url
                title = " ".join(title)
                item['title'] = " ".join(title.split())

                data_text = post.xpath('string()').extract()                
                data_text = " ".join(data_text)
                item['text'] = " ".join(data_text.split())
                yield item
