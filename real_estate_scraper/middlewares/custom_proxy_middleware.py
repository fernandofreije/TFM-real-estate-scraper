import scrapy


class CustomProxyMiddleware(object):
    def process_request(self, request, spider):
        scrapy.Request('http://www.freeproxylists.net/?c=&pt=&pr=HTTPS&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=70'))

        request.meta[“proxy”]="http://192.168.1.1:8050"
