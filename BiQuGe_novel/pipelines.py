# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
import pymongo

from scrapy.conf import settings


class BiqugeNovelPipeline(object):
    def __init__(self):
        self.f = open('1.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(content)
        self.f.write(',\n')
        return item

    def close_spider(self,spider):
        self.f.close()


class MysqlbinPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(
            user='root',
            passwd='baipengbin',
            host='localhost',
            port=3306,
            db='scrapy_info',
            charset='utf8'
        )

    def process_item(self, item, spider):
        name = item['name']
        author = item['author']
        chapter = item['chapter_name']
        content = item['content']

        cursor = self.connection.cursor()
        sql = "insert into novel(bookName, bookAuthor, chapter, content) VALUES ('%s', '%s', '%s', '%s')" % (name, author, chapter, content)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return item


class Mongodb(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        database_name = settings['MONGODB_DATABASE']
        collection_name = settings['MONGODB_COLLECTION']

        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[database_name]
        self.mycollection = mydb[collection_name]

    def process_item(self, item, spider):
        self.mycollection.insert(dict(item))
        return item
