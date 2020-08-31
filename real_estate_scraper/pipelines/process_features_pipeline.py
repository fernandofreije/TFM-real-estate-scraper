import re


def only_digits(text):
    return re.sub(r'\D', "", text)


class ProcessFeaturesPipeline:
    def process_item(self, item, spider):
        item['price'] = only_digits(item['price'])
        for char in item['features']:
            if 'm²' in char.lower() and '€' not in char.lower():
                item['size'] = int(only_digits(char))
            elif 'planta' in char.lower():
                item['floor'] = int(only_digits(char))
            elif 'nueva' in char.lower():
                item['new_development'] = True

        del item['features']
        return item
