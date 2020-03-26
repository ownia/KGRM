from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import time
from fake_useragent import UserAgent

chrome_driver = 'C:\\Users\\o4516\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\selenium' \
                '\\webdriver\\chrome\\chromedriver.exe '
chrome_options = Options()
chrome_options.binary_location = 'C:\\Program Files (x86)\\Google\\Chrome Dev\\Application\\chrome.exe'
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)
# ua=UserAgent()
reader = csv.reader(open('kd.csv', encoding='utf-8'))
f = open(r"industry.csv", 'w', encoding='utf-8', newline="")
csv_writer = csv.writer(f)
csv_writer.writerow(["company name", "industry", "registered", "scale"])
com_name_list = []
hy_list = []
registered_list = []
scale_list = []
i = 0
for row in reader:
    i += 1
    com_name = row[0]
    first_url = "https://xin.baidu.com/s?q=%s" % com_name
    driver.get(first_url)
    time.sleep(2)
    try:
        detail_url_tag = driver.find_element_by_xpath(
            '//div[@class="zx-viewport"]//div[@class="zx-content-wrap"] //div[@class="zx-content"]//div['
            '@class="zx-list-wrap"]//div[@class="zx-list-content"]//div[@class="zx-list-item"][1]//div['
            '@class="zx-ent-info"]/div/h3/a')
        detail_url = detail_url_tag.get_attribute('href')
        print(detail_url)
        driver.get(detail_url)
    except:
        scale = "None"
        hy = "None"
        registered = "0"
    try:
        scale_tag = driver.find_element_by_xpath(
            '//div[@class="zx-viewport"]//div[@class="zx-content-wrap"]//div[@class="zx-content"]//div['
            '@class="zx-detail-content"]//div[@class="zx-detail-wrap"]//div[@class="zx-detail-item show"]//div['
            '@class="zx-detail-basic"]//div[@id="basic-business"]/div/table/tbody/tr[10]/td/p')
        scale = scale_tag.get_attribute("data-content")
    except:
        scale = "None"
    try:
        registered_tag = driver.find_element_by_xpath(
            '//div[@class="zx-viewport"]//div[@class="zx-content-wrap"]//div[@class="zx-content"]//div['
            '@class="zx-detail-content"]//div[@class="zx-detail-wrap"]//div[@class="zx-detail-item show"]//div['
            '@class="zx-detail-basic"]//div[@id="basic-business"]/div/table/tbody/tr[1]/td[2]')
        registered = registered_tag.text
    except:
        registered = "0"
    try:
        hy_tag = driver.find_element_by_xpath(
            '//div[@class="zx-viewport"]//div[@class="zx-content-wrap"]//div[@class="zx-content"]//div['
            '@class="zx-detail-content"]//div[@class="zx-detail-wrap"]//div[@class="zx-detail-item show"]//div['
            '@class="zx-detail-basic"]//div[@id="basic-business"]/div/table/tbody/tr[3]/td[4]')
        hy = hy_tag.text
    except:
        hy = "None"
    print(com_name)
    print(hy)
    print(registered)
    print(scale)
    com_name_list = com_name_list + [com_name]
    hy_list = hy_list + [hy]
    registered_list = registered_list + [registered]
    scale_list = scale_list + [scale]
    csv_writer.writerow([com_name_list[i - 1], hy_list[i - 1], registered_list[i - 1], scale_list[i - 1]])
f.close()
