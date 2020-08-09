from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import logging


class MongoPipeline:
    def __init__(self):
        settings = get_project_settings()
        connection = MongoClient(
            settings['MONGODB_CONNECTION_STRING']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        logging.debug(f"Added item with id {item['description']}")
        return item
