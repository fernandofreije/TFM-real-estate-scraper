from scrapy.exceptions import DropItem


class FilterPipeline:
    def process_item(self, item, spider):
        if not item['remote_id']:
            raise DropItem('Missing Remote Id')
        return item
