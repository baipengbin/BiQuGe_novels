# -*- coding: utf-8 -*-
import scrapy

from BiQuGe_novel.items import NovelItem


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['biquge5200.com']
    start_urls = [
        # 'https://www.biquge5200.com/xuanhuanxiaoshuo/',
        # 'https://www.biquge5200.com/xiuzhenxiaoshuo/',
        # 'https://www.biquge5200.com/doushixiaoshuo/',
        'https://www.biquge5200.com/chuanyuexiaoshuo/',
        # 'https://www.biquge5200.com/wangyouxiaoshuo/',
        # 'https://www.biquge5200.com/kehuanxiaoshuo/',
    ]

    def parse(self, response):
        # | //div[@class="r"]//span[@class="s2"]/a
        # 获取当前类型下所有的小说URL链接
        item = NovelItem()
        novel_list = response.xpath('//div[@class="l"]//span[@class="s2"] ')
        for each in novel_list:
            name = each.xpath('a/text()').extract_first()
            novel_url = each.xpath('a/@href').extract_first()
            item['name'] = name
            yield scrapy.Request(novel_url, meta={'item': item}, callback=self.get_chapters)
            break

    # 获取小说所有的章节名称及URL链接，小说作者
    def get_chapters(self, response):
        item = response.meta['item']
        author = response.xpath('//div[@id="info"]//p[1]/text()').extract_first()
        item['author'] = author.replace('&nbsp;', '').replace('\xa0', '')
        chapter_url_list = response.xpath('//div[@id="list"]/dl/dd')
        for each in chapter_url_list:
            chapter_name = each.xpath('a/text()').extract_first()
            chapter_url = each.xpath('a/@href').extract_first()
            item['chapter_name'] = chapter_name
            yield scrapy.Request(chapter_url, meta={"item": item}, callback=self.get_chapter_content)

    def get_chapter_content(self, response):
        item = response.meta["item"]
        content = response.xpath('//div[@id="content"]/text()').extract()
        content = ''.join(content).replace('　　', '').replace('readx;', '').replace('想看好看的小说，请使用微信关注公众号“得牛看书”。\r\n        ', '')
        item['content'] = content
        print(dict(item))
        yield item
