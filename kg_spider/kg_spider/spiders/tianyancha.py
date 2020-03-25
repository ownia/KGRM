import requests
from lxml import etree
import random
import re
import csv
import pandas as pd
# from multiprocess import Pool
# import HTMLParser
from html.parser import HTMLParser
from fake_useragent import UserAgent

# ua=UserAgent()

def down_load(url):
    cc = requests.get(url=url, headers=headers, proxies=proxy, verify=True)  # ,proxies=proxy,verify=True
    # cc=etree.HTML(cc)
    # cc.encode("utf-8").decode("utf-8")

    cc.encoding = "utf-8"
    return cc.text


# padas 转化成list
content = pd.read_csv("kd.csv", encoding="utf-8").values.tolist()

gs = []

for m in range(len(content) + 1):
    i = content[m][0]

    # i=input("请输入企业相关信息（企业名、工商号或纳税人号）：")
    first_url = "https://m.tianyancha.com/search?key=%s" % i
    # first_url="http://www.baidu.com"
    a = down_load(first_url)
    a = etree.HTML(a)
    detail_url = a.xpath('//div[contains(@class,"col-xs-10")]/a/@href')[0]
    # boss=a.xpath('//div[@class="search_row_new_mobil"]//a/text()')[0]

    if a.xpath('/html/body/div[3]/div[3]/div[1]/div[4]/div/div/div[4]/span/text()') == "未公开" or a.xpath(
            '/html/body/div[3]/div[3]/div[1]/div[4]/div/div/div[4]/span/text()') == "仍注册" or \
            a.xpath('//div[@class="search_row_new_mobil"]/div/div[2]/span/text()')[0] == "-" or \
            a.xpath('//div[@class="search_row_new_mobil"]/div/div[3]/span/text()')[0] == "-":

        pass
    else:
        the_registered_capital = a.xpath('//div[@class="search_row_new_mobil"]/div/div[2]/span/text()')[0]
        the_registered_time = a.xpath('//div[@class="search_row_new_mobil"]/div/div[3]/span/text()')[0]
        boss = a.xpath('//div[@class="search_row_new_mobil"]//a/text()')[0]
        print(detail_url)

        aa = down_load(detail_url)
        bb = etree.HTML(aa)
        try:
            company = bb.xpath('//div[@class="over-hide"]/div/text()')[0]
            # industry = re.findall("行业：</span><span>(.*?)</span></div>", aa, re.S)[0]
            the_enterprise_type = re.findall("企业类型：</span><span>(.*?)</span></div>", aa, re.S)[0]
            registration_number = re.findall("工商注册号：</span><span>(.*?)</span></div>", aa, re.S)[0]
            organization_code = re.findall("组织结构代码：</span><span>(.*?)</span></div>", aa, re.S)[0]
            credit_code = re.findall("统一信用代码：</span><span>(.*?)</span></div>", aa, re.S)[0]
            business_period = re.findall("经营期限：</span><span>(.*?)</span></div>", aa, re.S)[0]
            # approval_date = aa.xpath('/html/body/div[3]/div[1]/div[7]/div/div[11]/span[2]/text()')[0]
            registration_authority = re.findall("登记机关：</span><span>(.*?)</span></div>", aa, re.S)[0]
            registered_address = re.findall("注册地址：</span><span>(.*?)</span></div>", aa, re.S)[0]
            scope_of_business = re.findall('<text class="tyc-num">(.*?)</text>', aa, re.S)[0]
            h = HTMLParser()  # &#xxx;‘ 的格式其实是unicode，&#后面跟的是unicode字符的十进制值，解决字体这样的方法
            scope_of_business = h.unescape(scope_of_business)
            new = [str(m + 1), company, boss, the_registered_time, the_registered_capital,
                   the_enterprise_type, registration_number, organization_code,
                   credit_code, business_period, registration_authority,
                   registered_address, scope_of_business]
            print(m + 1)
            # gs1[ii+1]=["公司名："+company,"法人："+boss[ii],"注册时间："+the_registered_time[ii],"注册资本："+the_registered_capital[ii],"企业类型："+the_enterprise_type,"工商注册号："+registration_number,"组织结构代码："+organization_code,"统一信用代码："+credit_code,"经营年限："+business_period,"登记机关："+registration_authority,"注册地址："+registered_address,"经营范围："+scope_of_business]
            gs.append(new)
              # 抛出异常
        except:

            with open("5006663.csv", "w", encoding="utf-8", newline="") as f:
                k = csv.writer(f, dialect="excel")
                k.writerow(
                    ["编号", "公司名", "法人", "注册时间", "注册资本", "企业类型", "工商注册号", "组织结构代码", "统一信用代码", "经营年限", "登记机关", "注册地址",
                     "经营范围"])

                for list in gs:
                    k.writerow(list)

with open("500666666666.csv", "w", encoding="utf-8", newline="") as f:
    k = csv.writer(f, dialect="excel")
    k.writerow(["编号", "公司名", "法人", "注册时间", "注册资本", "企业类型", "工商注册号", "组织结构代码", "统一信用代码", "经营年限", "登记机关", "注册地址", "经营范围"])

    for list in gs:
        k.writerow(list)
# print(gs)

# print(gs1)
