# -*- coding: utf-8 -*-
import scrapy


class Kuaidi100Spider(scrapy.Spider):
    name = 'kuaidi100'
    # allowed_domains = ['kuaidi100.com']
    start_urls = ['https://www.kuaidi100.com/all/']

    def parse(self, response):
        kd1 = response.xpath('//div[@class="column-1 column-list"]/dl/dd')
        for each in kd1:
            yield {
                'name': each.xpath('.//a/text()').get()
            }
            yield {
                'name': each.xpath('.//a/following::a/text()').get()
            }
            yield {
                'name': each.xpath('.//a/following::a/following::a/text()').get()
            }
        kd2 = response.xpath('//div[@class="column-2 column-list"]/dl/dd')
        for each in kd2:
            yield {
                'name': each.xpath('.//a/text()').get()
            }
            yield {
                'name': each.xpath('.//a/following::a/text()').get()
            }
            yield {
                'name': each.xpath('.//a/following::a/following::a/text()').get()
            }
