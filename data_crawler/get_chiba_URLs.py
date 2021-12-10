from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pickle
from tqdm import tqdm
import time

SAVED_PATH = "./urls/chiba_urls.pickle"

def main():

    # Chrome のオプションを設定する
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    # Selenium Server に接続する
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=options.to_capabilities(),
        options=options,
    )

    chiba_data_urls = []

    pre_urls = [
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category1&pg=1",
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category2&pg=1", 
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category3&pg=1", 
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category4&pg=1", 
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category5&pg=1", 
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category6&pg=1", 
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category7&pg=1", 
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category8&pg=1", 
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category9&pg=1",
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category10&pg=1",
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category11&pg=1",
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category12&pg=1",
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category13&pg=1",
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category14&pg=1",
        "https://www.pref.chiba.lg.jp/gyoukaku/opendata/result-opendata.html?keyword=&category=category15&pg=1",
    ]

    for row_idx, url_row in enumerate(pre_urls):
        # if not row_idx == 26:
        #     continue
        # Selenium 経由でブラウザを操作する
        driver.get(url_row)
        driver.implicitly_wait(10)

        for i in range(20):
            url_elements = driver.find_elements_by_xpath("//div[@class='opendata_search_result_box']/div/div/a")
            for url_element in url_elements:
                url = url_element.get_attribute('href')
                chiba_data_urls.append(url)
                print(url)

            time.sleep(1)
            try:
                next_page_button = driver.find_element_by_xpath("//*[@id='opendata_pagination']/li[12]/a")
                next_page_button.click()          
            except:
                break
        # for drop_down_id in range(1, len(years_select.options)):
            

        #     years_select.select_by_index(drop_down_id)
        #     buttun_element = driver.find_elements_by_xpath("//div[@class='opendata_search_result_box']/div")
            
        #     driver.implicitly_wait(5)

        #     ActionChains(driver).move_to_element(buttun_element).click(buttun_element).perform()

        #     driver.implicitly_wait(5)

        #     try:
        #         data_titles = driver.find_element_by_class_name('data-title')
        #         url_element = data_titles.find_elements_by_xpath("a")
        #         for data_url in url_element:
        #             nagano_data_urls.append(data_url.get_attribute('href'))
        #     except:
        #         pass

    # ブラウザを終了する
    driver.quit()
    print(len(chiba_data_urls))
    with open(SAVED_PATH, "wb") as f:
        pickle.dump(chiba_data_urls, f)


if __name__=="__main__":
    main()