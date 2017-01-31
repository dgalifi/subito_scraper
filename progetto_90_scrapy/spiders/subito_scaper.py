# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.loader import ItemLoader
from progetto_90_scrapy.items import SubitoSingleItemList


class SubitoScaperSpider(scrapy.Spider):
    name = "subito"
    allowed_domains = ["subito.it"]
    start_urls = ['http://www.subito.it/annunci-italia/vendita/moto-e-scooter/?q=bmw+ninet']

    def parse(self, response):
        desc_list = response.css('div.item_description')
        logging.debug('Elementi nel listato: {0}'.format(len(desc_list), '>20'))
        current_item = SubitoSingleItemList()
        for desc in desc_list:
            current_item['category'] = desc.css('span.item_category::text').extract_first()
            current_item['title'] = desc.css('h2>a::attr(title)').extract_first()
            current_item['name'] = desc.css('h2>a::attr(name)').extract_first()
            current_item['link'] = desc.css('h2>a::attr(href)').extract_first()
            yield current_item
            # yield {
            #     'category': desc.css('span.item_category::text').extract_first(),
            #     'title': desc.css('h2>a::attr(title)').extract_first(),
            #     'name': desc.css('h2>a::attr(name)').extract_first(),
            #     'link': desc.css('h2>a::attr(href)').extract_first(),
            # }

        next_page = response.css('div.pagination_next>a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
