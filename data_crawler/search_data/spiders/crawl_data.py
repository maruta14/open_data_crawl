# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from search_data.items import SearchDataItem
import pickle



tochigi_urls_path = "../../../urls/tochigi_urls.pickle"
hyogo_urls_path = "../../../urls/hyogo_urls.pickle"

PREFECTURES_PARAMETER = {
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
        # 'start_urls' : ['http://tochigiken.jp/?page_id=18'],
        'title_css' : 'body',
        # 'title_css' : 'div#mdb_detail_print_20 > table > tr:nth-child(1) > td > table > tr:nth-child(1) > td::text',
        'text_css' : 'body'
    },
    "gunma_1p": {
        'allowed_domains' : [],
        'start_urls' : ['https://www.pref.gunma.jp/07/b2700058.html#tiri1'],
        'restrict_css' : 'div#scroll-main > article > div > table tbody > tr > td:nth-child(4)',
        #scroll-main > article > div:nth-child(3)
        #scroll-main > article > div:nth-child(4) > table > tbody > tr:nth-child(1) > td:nth-child(4)
        # 'deny_rule' : r"/.+\.(csv|shp|shx|dbf|xls|prj|sbx|xml|sbn)",
        'title_css' : 'head > title::text',
        'text_css' : 'body',
        "depth_limit" : 2
    },
    "gunma_all_p": {
        'allowed_domains' : ['www.pref.gunma.jp'],
        'start_urls' : ['https://www.pref.gunma.jp/07/b2700058.html#tiri1'],
        'restrict_css' : '#scroll-main > article > div:nth-child(3) > ol:nth-child(2) > li:nth-child(1) > a',
        "depth_limit" : 0
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
        'start_urls' : ['https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category1&pg=5'],
        # 'rule' : r'/result.opendata.html.keyword..category.category[0-9].pg.[0-9]+',
        'rule' : r'/gyoukaku/opendata/result-opendata.html.keyword=.category=category[0-9]&pg=[0-9]+',
        # 'restrict_css' : '#tmp_opendata_full > div.opendata_search_result_box',
        # 'restrict_css' : '#tmp_rcnt > div > div > div#tmp_contents',
        'rule2' : r'/opendata-.*\.html',
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
        'text_css' : '#main_body',
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
        'rule2' : r'/statist_list/[0-9]+\.html',
        # 'rule3' : r'/statistics/[0-9]+\.html',
        # 'restrict_css' : '#search-item-list-box',
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
    "shizuoka": {
        'allowed_domains' : ['opendata.pref.shizuoka.jp'],
        'start_urls' : ['https://opendata.pref.shizuoka.jp/dataset/search?page=5', 'https://opendata.pref.shizuoka.jp/dataset/search?page=14',
                        'https://opendata.pref.shizuoka.jp/dataset/search?page=23', 'https://opendata.pref.shizuoka.jp/dataset/search?page=32', 
                        'https://opendata.pref.shizuoka.jp/dataset/search?page=41', 'https://opendata.pref.shizuoka.jp/dataset/search?page=50', 
                        'https://opendata.pref.shizuoka.jp/dataset/search?page=59', 'https://opendata.pref.shizuoka.jp/dataset/search?page=68', 
                        'https://opendata.pref.shizuoka.jp/dataset/search?page=77', 'https://opendata.pref.shizuoka.jp/dataset/search?page=86', 
                        'https://opendata.pref.shizuoka.jp/dataset/search?page=95', 'https://opendata.pref.shizuoka.jp/dataset/search?page=104', 
                        'https://opendata.pref.shizuoka.jp/dataset/search?page=113', 'https://opendata.pref.shizuoka.jp/dataset/search?page=122',
                        'https://opendata.pref.shizuoka.jp/dataset/search?page=131',     
                        ],
        'rule1' : r'/dataset/search.page=[0-9]+',
        'rule2' : r'/dataset/.*\.html',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",    
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
        'allowed_domains' : [],
        'start_urls' : ['https://www.pref.mie.lg.jp/common/06/ci500003936.htm'],
        'rule' : r'/IT/HP/[0-9]+\.htm',
        # 'restrict_css' : '#center-contents',
        # 'restrict_css2' : '#section1 > div > div > div.table-swipe-wrap > table',
        'restrict_css2' : '#section1',
        'title_css' : 'head > title::text',
        'text_css' : '#center-contents > div.section',
        "depth_limit" : 2   
    },
    "shiga": {
        'allowed_domains' : ['www.pref.shiga.lg.jp'],
        'start_urls' : ['https://www.pref.shiga.lg.jp/ippan/kurashi/ict/300002.html'],
        'rule' : r'/ippan/kurashi/ict/[0-9]+.html',
        'restrict_css' : 'body > div.cms-public > div > div > div.area-group-2-3-4 > div.area.area3 > div:nth-child(1) > div > div:nth-child(13)',
        'title_css' : 'head > title::text',
        'text_css' : 'body > div.cms-public > div > div > div.area-group-2-3-4 > div.area.area3 > div.parts',
        "depth_limit" : 2   
    },
    "kyoto": {
        'allowed_domains' : ['data.pref.kyoto.lg.jp'],
        # 'start_urls' : ['https://data.pref.kyoto.lg.jp/dataset?page=4'],

        'start_urls' : ['https://data.pref.kyoto.lg.jp/dataset?page=4', 'https://data.pref.kyoto.lg.jp/dataset?page=9', 'https://data.pref.kyoto.lg.jp/dataset?page=14',
                        'https://data.pref.kyoto.lg.jp/dataset?page=19', 'https://data.pref.kyoto.lg.jp/dataset?page=24', 'https://data.pref.kyoto.lg.jp/dataset?page=29',
                        'https://data.pref.kyoto.lg.jp/dataset?page=34', 'https://data.pref.kyoto.lg.jp/dataset?page=38'],
        'rule' : r'/dataset.page=[0-9]+',
        'restrict_css' : '#content > div.row.wrapper > div > section:nth-child(1) > div.module-content > ul > li > div',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "osaka": {
        'allowed_domains' : ['data.bodik.jp'],
        'start_urls' : ['https://data.bodik.jp/organization/270008?page=2'],
        'rule' : r'/organization/270008.page=[1-3]',
        'restrict_css' : '#content > div.row.wrapper > div > article > div > ul',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "hyogo": {
        'allowed_domains' : ['open-data.pref.hyogo.lg.jp'],
        'title_css' : 'head > title::text',
        'text_css' : '#_centercolumn'
    },
    "nara": {
        'allowed_domains' : ['www.pref.nara.jp'],
        'start_urls' : ['https://www.pref.nara.jp/44954.htm'],
        'restrict_css' : r'#ContentPane > div:nth-child(22) > div > div.inside_b > div',
        'restrict_css2' : '#ContentPane > div:nth-child(5) > div > div.inside_b > div > table > tbody',
        'title_css' : 'head > title::text',
        'text_css' : '#ContentPane > div:nth-child(5) > div > div.inside_b > div > table'
    },
    "wakayama": {
        'allowed_domains' : ['data.bodik.jp'],
        'start_urls' : ['https://data.bodik.jp/organization/300004?page=1'],
        'rule' : r'/organization/300004.page=[1-3]',
        'restrict_css' : '#content > div.row.wrapper > div > article > div > ul',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "tottori": {
        'allowed_domains' : ['odp-pref-tottori.tori-info.co.jp'],
        'start_urls' : ['https://odp-pref-tottori.tori-info.co.jp/dataset/search/index.p5.html'],
        'rule' : r'search/index\.p[0-9]+\.html',
        'rule2' : r'/dataset/[0-9]+\.html',
        'restrict_css' : '#content > div.row.wrapper > div > article > div > ul',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",
        'title_css' : 'head > title::text',
        'text_css' : '#main > div.text',
        'text_css2' : '#main > div.dataset-tabs',
        "depth_limit" : 2
    },
    "shimane": {
        'allowed_domains' : ['shimane-opendata.jp'],
        'start_urls' : ['https://shimane-opendata.jp/db/organization/main?page=4'],
        'rule' : r'/db/organization/main.page=[0-9]+',
        'restrict_css' : '#content > div.row.wrapper > div > article > div > ul',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div > div',
        'text_css2' : '#dataset-resources > ul > li',
        'text_css3' : '#content > div.row.wrapper > div > article > div > section.additional-info',
        "depth_limit" : 2
    },
    "okayama": {
        'allowed_domains' : ['www.okayama-opendata.jp'],
        'start_urls' : ['https://www.okayama-opendata.jp/datasets?page=6', 'https://www.okayama-opendata.jp/datasets?page=12',
                        'https://www.okayama-opendata.jp/datasets?page=19', 'https://www.okayama-opendata.jp/datasets?page=26', 
                        'https://www.okayama-opendata.jp/datasets?page=33', 'https://www.okayama-opendata.jp/datasets?page=40', 
                        'https://www.okayama-opendata.jp/datasets?page=47'],
        'rule' : r'/datasets.page=[0-9]+',
        'rule2' : r'/datasets/[0-9]+',
        'title_css' : 'head > title::text',
        'text_css' : 'body > div > div:nth-child(2) > div > div.l-row > div.l-main > div',
        "depth_limit" : 2
    },
    "hiroshima": {
        'allowed_domains' : ['www.pref.hiroshima.lg.jp'],
        'start_urls' : ['https://www.pref.hiroshima.lg.jp/soshiki/265/opendata.html'],
        'rule' : r'/soshiki/265/opendata-.+\.html',
        "depth_limit" : 1
    },
    "yamaguchi": {
        'allowed_domains' : ['yamaguchi-opendata.jp'],
        'start_urls' : ['https://yamaguchi-opendata.jp/ckan/dataset?page=4'],
        'rule' : r'/dataset.page=[0-9]+',
        'restrict_css' : '#content > div.row.wrapper > div > section:nth-child(1) > div.module-content > ul',
        'deny_rule' : r"/dataset/.*(resource|groups|activity).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "tokushima": {
        'allowed_domains' : ['ouropendata.jp'],
        'start_urls' : ['https://ouropendata.jp/dataset/search/index.p5.html', 'https://ouropendata.jp/dataset/search/index.p14.html', 
                        'https://ouropendata.jp/dataset/search/index.p23.html', 'https://ouropendata.jp/dataset/search/index.p32.html', 
                        'https://ouropendata.jp/dataset/search/index.p41.html', 'https://ouropendata.jp/dataset/search/index.p50.html', 
                        'https://ouropendata.jp/dataset/search/index.p59.html', 'https://ouropendata.jp/dataset/search/index.p68.html', 
                        'https://ouropendata.jp/dataset/search/index.p76.html'],
        'rule' : r'/dataset/search/index.p[0-9]+\.html',
        'rule2' : r'/dataset/[0-9]+\.html',
        'deny_rule' : r"/dataset/[0-9]+\.html#cms-tab-7-[1-2]-view",
        'title_css' : 'head > title::text',
        'text_css' : '#main',
        "depth_limit" : 2
    },
    "kagawa": {
        'allowed_domains' : ['opendata.pref.kagawa.lg.jp'],
        'start_urls' : ['https://opendata.pref.kagawa.lg.jp/dataset/search/index.p5.html', 'https://opendata.pref.kagawa.lg.jp/dataset/search/index.p14.html', 
                        'https://opendata.pref.kagawa.lg.jp/dataset/search/index.p23.html'],
        'rule' : r'/dataset/search/index.p[0-9]+\.html',
        'rule2' : r'/dataset/[0-9]+\.html',
        'deny_rule' : r"/dataset/[0-9]+\.html#cms-tab-7-[1-2]-view",
        'title_css' : 'head > title::text',
        'text_css' : '#main > div.text',
        'text_css3' : '#main > nav',
        'text_css2' : '#dataset-tabs-7',
        "depth_limit" : 2
    },
    "kochi": {
        'allowed_domains' : ['www.pref.kochi.lg.jp'],
        'start_urls' : ['https://www.pref.kochi.lg.jp/opendata/'],
        'rule' : r'/opendata/docs/.*/',
    },
    "hukuoka": {
        'allowed_domains' : ['ckan.open-governmentdata.org'],
        'start_urls' : ['https://ckan.open-governmentdata.org/organization/fukuoka-pref?page=4', 'https://ckan.open-governmentdata.org/organization/fukuoka-pref?page=9', 
                        'https://ckan.open-governmentdata.org/organization/fukuoka-pref?page=14', 'https://ckan.open-governmentdata.org/organization/fukuoka-pref?page=19', 
                        'https://ckan.open-governmentdata.org/organization/fukuoka-pref?page=24', 'https://ckan.open-governmentdata.org/organization/fukuoka-pref?page=29'],
        'rule' : r'/organization/fukuoka-pref.page=[0-9]+',
        'rule2' : r'/dataset/.*',
        'deny_rule' : r"/dataset/.*(resource|groups|activity|showcases).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "saga": {
        'allowed_domains' : ['data.bodik.jp'],
        'start_urls' : ['https://data.bodik.jp/organization/410004?page=4', 'https://data.bodik.jp/organization/410004?page=9', 
                        'https://data.bodik.jp/organization/410004?page=14', 'https://data.bodik.jp/organization/410004?page=19', 
                        'https://data.bodik.jp/organization/410004?page=24'],
        'rule' : r'/organization/410004.page=[0-9]+',
        'rule2' : r'/dataset/.*',
        'deny_rule' : r"/dataset/.*(resource|groups|activity|showcases).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "nagasaki": {
        'allowed_domains' : ['data.bodik.jp'],
        'start_urls' : ['https://data.bodik.jp/organization/420000?page=4', 'https://data.bodik.jp/organization/420000?page=4'],
        'rule' : r'/organization/420000.page=[0-9]+',
        'rule2' : r'/dataset/.*',
        'deny_rule' : r"/dataset/.*(resource|groups|activity|showcases).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "kumamoto": {
        'allowed_domains' : ['www.pref.kumamoto.jp'],
        'start_urls' : ['https://www.pref.kumamoto.jp/soshiki/211/'],
        'rule' : r'/82808.html',
        "depth_limit" : 1
    },
    "oita": {
        'allowed_domains' : ['data.bodik.jp'],
        'start_urls' : ['https://data.bodik.jp/organization/440001?page=4', 'https://data.bodik.jp/organization/440001?page=9'],
        'rule' : r'/organization/440001.page=[0-9]+',
        'rule2' : r'/dataset/.*',
        'deny_rule' : r"/dataset/.*(resource|groups|activity|showcases).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "miyazaki": {
        'allowed_domains' : ['data.bodik.jp'],
        'start_urls' : ['https://data.bodik.jp/organization/450006?page=4', 'https://data.bodik.jp/organization/450006?page=9', 
                        'https://data.bodik.jp/organization/450006?page=14', 'https://data.bodik.jp/organization/450006?page=19', 
                        'https://data.bodik.jp/organization/450006?page=24'],
        'rule' : r'/organization/450006.page=[0-9]+',
        'rule2' : r'/dataset/.*',
        'deny_rule' : r"/dataset/.*(resource|groups|activity|showcases).*",
        'title_css' : 'head > title::text',
        'text_css' : '#content > div.row.wrapper > div > article > div',
        "depth_limit" : 2
    },
    "kagoshima": {
        'allowed_domains' : ['www.pref.kagoshima.jp'],
        'start_urls' : ['http://www.pref.kagoshima.jp/ac03/infra/info/opendata/index.html'],
        'rule' : r'/opendata/.*/index.html',
        'restrict_css' : '#tmp_contents',
        'title_css' : 'head > title::text',
        'text_css' : '#tmp_contents',
        "depth_limit" : 2
    },
    "okinawa": {
        'allowed_domains' : ['www.pref.okinawa.jp'],
        'start_urls' : ['https://www.pref.okinawa.jp/site/kikaku/joho/kikaku/opendata/opendate_top.html'],
        'restrict_css' : '#tmp_contents',
        "depth_limit" : 1
    },

}


class CrawlDataSpider(CrawlSpider):
    name = 'crawl_data'
    prefecture = 'chiba'
    pre_rules = PREFECTURES_PARAMETER[prefecture]


    allowed_domains = pre_rules['allowed_domains']

    if prefecture == 'tochigi':
        with open(tochigi_urls_path, "rb") as f:
            start_urls = pickle.load(f)
    elif prefecture == 'hyogo':
        with open(hyogo_urls_path, "rb") as f:
            start_urls = pickle.load(f)

    else:
        start_urls = pre_rules['start_urls']


    rules = (
        # 正規表現にマッチするリンクをクローリング
        Rule(LinkExtractor(allow=pre_rules['rule'])),
        Rule(LinkExtractor(allow=pre_rules['rule2']), follow=True, callback='parse_item'),
        # Rule(LinkExtractor(allow=pre_rules['rule3'])),
        # # # 正規表現にマッチするリンクをparseメソッドでスクレイピング
        # Rule(LinkExtractor(restrict_css=pre_rules['restrict_css']), follow=True, callback='parse_item'),
        # Rule(LinkExtractor(restrict_css=pre_rules['restrict_css']), follow=True, callback='parse_item')
    )
    

    def parse_item(self, response):
        item = SearchDataItem()
        item['url'] = response.url
        # title = response.css(self.pre_rules['title_css']).extract()
        # item['title'] = [" ".join(title[0].split())]
        # data_text = response.css(self.pre_rules['text_css']).xpath('string()').extract()

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
            
        
        # data_text = " ".join(data_text)
        # item['text'] = " ".join(data_text.split())
        # print(item['title'], item['text'])

        return item


    def parse_okinawa(self, response):
        item = SearchDataItem()
        for quote in response.css("#tmp_contents > table > tbody > tr"):
            title = quote.css("td:nth-child(4)").xpath('string()').extract()
            if len(title) == 0:
                continue
            item['url'] = response.url
            title = " ".join(title)
            item['title'] = " ".join(title.split())

            data_text = quote.xpath('string()').extract()
            data_text = " ".join(data_text)
            data_text = " ".join(data_text.split())
            item['text'] = data_text
            if "xls" in " ".join(data_text.split()) or "csv" in " ".join(data_text.split()):
                item['text'] = " ".join(data_text.split())
                yield item



    def parse_kumamoto(self, response):
        item = SearchDataItem()
        for quote in response.css("#main_body > div.detail_free > table > tbody > tr"):
            title = quote.css("td:nth-child(1)").xpath('string()').extract()
            if len(title) == 0:
                continue
            item['url'] = response.url
            title = " ".join(title)
            item['title'] = " ".join(title.split())

            data_text = quote.xpath('string()').extract()
            data_text = " ".join(data_text)
            data_text = " ".join(data_text.split())
            item['text'] = data_text
            if "CSV" in " ".join(data_text.split()):
                item['text'] = " ".join(data_text.split())
                yield item



    def parse_kochi(self, response):
        item = SearchDataItem()
        for quote in response.css("#contentBody > article > div.body > table > tbody > tr"):
            title = quote.css("td:nth-child(1)").xpath('string()').extract()
            if len(title) == 0:
                continue
            item['url'] = response.url
            title = " ".join(title)
            item['title'] = " ".join(title.split())

            data_text = quote.xpath('string()').extract()
            data_text = " ".join(data_text)
            data_text = " ".join(data_text.split())
            item['text'] = data_text
            if "XLS" in " ".join(data_text.split()):
                item['text'] = " ".join(data_text.split())
                yield item


    def parse_hiroshima(self, response):
        item = SearchDataItem()
        for quote in response.css("#main_body > div.detail_free"):
            for post in quote.css("tbody > tr"):
                title = post.css("td:nth-child(1)").xpath('string()').extract()
                if len(title) == 0:
                    continue
                item['url'] = response.url
                title = " ".join(title)
                item['title'] = " ".join(title.split())

                data_text = post.xpath('string()').extract()
                data_text = " ".join(data_text)
                data_text = " ".join(data_text.split())
                print(type(data_text))
                item['text'] = data_text
                yield item


    def parse_gunma(self, response):
        item = SearchDataItem()
        for quote in response.css("#scroll-main > article > div > table > tbody > tr"):
            # for post in quote.css("tbody > tr"):
                
            title = quote.css("td:nth-child(1)").xpath('string()').extract()
            if len(title) == 0:
                continue
            item['url'] = response.url
            title = " ".join(title)
            item['title'] = " ".join(title.split())

            data_text = quote.xpath('string()').extract()                
            data_text = " ".join(data_text)
            if "CSV" in " ".join(data_text.split()):
                item['text'] = " ".join(data_text.split())
                yield item
            elif "エクセル" in " ".join(data_text.split()):
                item['text'] = " ".join(data_text.split())
                yield item




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
