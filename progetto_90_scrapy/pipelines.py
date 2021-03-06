# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Progetto90ScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        #self.client = pymongo.MongoClient(self.mongo_uri)
        self.client = pymongo.MongoClient(self.mongo_uri, 27017)
        try:
            self.client['admin'].authenticate('davide', 'laCucc4r4cia', mechanism='SCRAM-SHA-1')
            self.db = self.client[self.mongo_db]
        except Exception as e:
            print('mongo db auth error %s' % e)
            #return self
        #self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        cursor = self.db[self.collection_name].find({'name':dict(item)['name']})

        if cursor.count() == 0:
            print(dict(item)['name'])
            print('New Doc! : {0}'.format(cursor.count()))
            self.db[self.collection_name].insert(dict(item))
        # else:
        #     # update date_scraped
        #     print('Numero duplicati: {0}'.format(cursor.count()))
        #     self.db[self.collection_name].update_one({'name': dict(item)['name']}, {'date_scraped': dict(item)['date_scraped']})
        # 
        return item
