class TypePipeline:
    def process_item(self, item, spider):
        item['price'] = int(item['price'].replace(
            '.', '')) if item['price'] is not None else item['price']
        item['rooms'] = int(item['rooms'].replace(
            '.', '')) if item['rooms'] is not None else item['rooms']
        item['baths'] = int(item['baths'].replace(
            '.', '')) if item['baths'] is not None else item['baths']
        item['real_estate_agent'] = item['real_estate_agent'] is not None
        item['link'] = f'https://www.pisos.com/{item["link"]}'
        item['category'] = 'piso' if 'piso' in item['description'].lower() else 'casa'

        return item
