# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    chapter_name = scrapy.Field()
    content = scrapy.Field()