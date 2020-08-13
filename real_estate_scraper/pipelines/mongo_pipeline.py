from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import logging
from datetime import datetime


class MongoPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.connection = MongoClient(
            settings['MONGODB_CONNECTION_STRING']
        )
        self.db = self.connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def spider_closed(self, spider, reason):
        self.connection.close()

    def process_item(self, item, spider):
        self.collection.find()
        if self.collection.find_one({'remote_id': item['remote_id']}):
            self.collection.update(
                {'remote_id': item['remote_id']},
                {'$set': {**dict(item), **{'updated_at': datetime.now()}}}
            )
            logging.info(f"Updated item with id -- {item['remote_id']}")
        else:
            self.collection.insert(
                {**dict(item), **{'created_at': datetime.now(),
                                  'updated_at': datetime.now()}}
            )
            logging.info(f"Added item with id -- {item['remote_id']}")

        return item
