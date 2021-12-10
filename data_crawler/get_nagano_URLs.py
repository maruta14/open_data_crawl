from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import glob
import csv
import pickle
from tqdm import tqdm

NAGANO_URL_PATH = "./search_data/spiders/nagano_pre_urls.csv"
SAVED_PATH = "./urls/nagano_urls.pickle"

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

    nagano_data_urls = []

    with open(NAGANO_URL_PATH, "r") as f:
        url_rows = csv.reader(f)
        for row_idx, url_row in tqdm(enumerate(url_rows)):
            # if not row_idx == 26:
            #     continue
            # Selenium 経由でブラウザを操作する
            driver.get(url_row[0])
            driver.implicitly_wait(20)

            years = driver.find_element_by_name("search_y")
            years_select = Select(years)
            for drop_down_id in range(1, len(years_select.options)):
                years_select.select_by_index(drop_down_id)
                buttun_element = driver.find_element_by_xpath("//button[@class='search_button']")
                
                driver.implicitly_wait(5)

                ActionChains(driver).move_to_element(buttun_element).click(buttun_element).perform()

                driver.implicitly_wait(5)

                try:
                    data_titles = driver.find_element_by_class_name('data-title')
                    url_element = data_titles.find_elements_by_xpath("a")
                    for data_url in url_element:
                        nagano_data_urls.append(data_url.get_attribute('href'))
                except:
                    pass

    # ブラウザを終了する
    driver.quit()
    with open(SAVED_PATH, "wb") as f:
        pickle.dump(nagano_data_urls, f)


if __name__=="__main__":
    main()