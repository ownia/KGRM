from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

# 读取公司名单CSV1
reader = csv.reader(open('kd.csv'))
# 打开存放数据的CSV2
f = open(r"industry.csv", 'w', encoding='utf-8', newline="")
csv_writer = csv.writer(f)
# 将表格标题写入CSV2
csv_writer.writerow(["company name", "industry", "scale"])
com_name_list = []
hy_list = []
scale_list = []
i = 0
for row in reader:
    i += 1
    com_name = row[0]
    first_url = "https://xin.baidu.com/s?q=%s" % com_name
    # 模拟搜索公司名称
    driver.get(first_url)
    # 静止三秒
    time.sleep(3)
    try:
        detail_url_tag = driver.find_element_by_xpath(
            '//div[@class="zx-viewport"]//div[@class="zx-content-wrap"] //div[@class="zx-content"]//div[@class="zx-list-wrap"]//div[@class="zx-list-content"]//div[@class="zx-list-item"][1]//div[@class="zx-ent-info"]/div/h3/a')
        detail_url = detail_url_tag.get_attribute('href')
        print(detail_url)
        driver.get(detail_url)
    except:
        scale = "None"
        hy = "None"
    try:
        # 检索包含经营范围的标签
        scale_tag = driver.find_element_by_xpath(
            '//div[@class="zx-viewport"]//div[@class="zx-content-wrap"]//div[@class="zx-content"]//div[@class="zx-detail-content"]//div[@class="zx-detail-wrap"]//div[@class="zx-detail-item show"]//div[@class="zx-detail-basic"]//div[@id="basic-business"]/div/table/tbody/tr[10]/td/p')
        scale = scale_tag.get_attribute("data-content")
    except:
        scale = "None"
    try:
        # 检索包含行业信息的标签
        hy_tag = driver.find_element_by_xpath(
            '//div[@class="zx-viewport"]//div[@class="zx-content-wrap"]//div[@class="zx-content"]//div[@class="zx-detail-content"]//div[@class="zx-detail-wrap"]//div[@class="zx-detail-item show"]//div[@class="zx-detail-basic"]//div[@id="basic-business"]/div/table/tbody/tr[3]/td[4]')
        hy = hy_tag.text
    except:
        hy = "None"
    print(com_name)
    print(hy)
    print(scale)
    com_name_list = com_name_list + [com_name]
    hy_list = hy_list + [hy]
    scale_list = scale_list + [scale]
    # 将公司名称、行业信息、经营范围信息写入CSV2
    csv_writer.writerow([com_name_list[i - 1], hy_list[i - 1], scale_list[i - 1]])
# 关闭CSV2
f.close()
