# -*- coding: utf-8 -*-
import scrapy
import sys


class PconlineSpider(scrapy.Spider):
    name = 'pconline'
    # allowed_domains = ['pconline.com.cn']
    start_urls = ['https://ks.pconline.com.cn/product.shtml?q=tcl']

    def parse(self, response):
        # item = PcoItem()
        pco = response.xpath('//div[@class="col-955"]/ul[@class="list-items list-type-tw"]/li[@class="item"]')
        for each in pco:
            yield {
                'name':
                    each.xpath(
                        './/div[@class="item-title"]/a[@class="item-name"]/@title').extract(),
                'content': each.xpath(
                    './/div[@class="item-title"]/span[@class="item-des"]/text()').extract()
            }

            next_page = response.xpath('//div[@class="page"]/a[@class="next"]/@href').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)
