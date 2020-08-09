
from itemadapter import ItemAdapter


class TypePipeline:
    def process_item(self, item, spider):
        item['price'] = int(item['price'].replace(
            '.', '')) if item['price'] is not None else item['price']
        item['rooms'] = int(item['rooms'].replace(
            '.', '')) if item['rooms'] is not None else item['rooms']
        item['baths'] = int(item['baths'].replace(
            '.', '')) if item['baths'] is not None else item['baths']

        return item
