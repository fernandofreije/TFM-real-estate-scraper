import scrapy


class RealEstateSpider(scrapy.Spider):
    name = "real_estate"

    def start_requests(self):
        urls = [
            'https://www.pisos.com/venta/pisos-asturias/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for real_estate in response.css('#parrilla .row'):
            real_estate.css('div.characteristics .item').getall()
            yield {
                'price': real_estate.css('div.price::text').get(),
                'location': real_estate.css('div.location::text').get(),
                'description': real_estate.css('.title a::text').get(),
                'rooms': real_estate.xpath("span[contains(@class,'icoBed')][ancestor::div[contains(@class, 'item')]]").get(),
                'baths': real_estate.xpath("span[contains(@class, 'icoBath')][ancestor::div[contains(@class, 'item')]]").get(),
                'features':  real_estate.css('div.characteristics div.item::text').getall(),
            }

        next_page_url = response.css(
            'div.pager span.item.selected + a.item::attr(href)').get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
