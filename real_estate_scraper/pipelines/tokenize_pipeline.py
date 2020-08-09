import re
from collections.abc import Iterable


class TokenizePipeline:
    def process_item(self, item, spider):
        p = re.compile('[\r\n]+')
        for k, v in item.items():
            if isinstance(v, Iterable) and not isinstance(v, str):
                item[k] = map(lambda x: p.sub('', x).replace(
                    ' ', ''), v) if v is not None else v
            else:
                item[k] = p.sub('', v).replace(' ', '') if v is not None else v
        return item
