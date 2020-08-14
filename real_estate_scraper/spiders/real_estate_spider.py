import logging
import scrapy
import yaml
from datetime import datetime
import pkgutil


class RealEstateSpider(scrapy.Spider):
    name = "real_estate"

    # logging.basicConfig(
    #     filename=f'logs/{datetime.now().timestamp()}.log',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO
    # )

    def start_requests(self):
        provinces_raw = pkgutil.get_data(
            "real_estate_scraper", "resources/provinces.yml")
        provinces = yaml.safe_load(provinces_raw)

        urls = [
            f'https://www.pisos.com/{operation}/pisos-{province}/' for operation in ['venta', 'alquiler'] for province in provinces.values()
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for real_estate in response.css('.parrilla-bg #parrilla.Listado .row'):
            real_estate.css('div.characteristics .item').getall()
            yield {
                'price': real_estate.css('div.price::text').get(),
                'location': real_estate.css('div.location::text').get(),
                'description': real_estate.css('.title a::text').get(),
                'rooms': real_estate.xpath(".//span[contains(@class, 'icoBed')]/parent::*/text()").get(),
                'baths': real_estate.xpath(".//span[contains(@class, 'icoBath')]/parent::*/text()").get(),
                'imageLink': real_estate.css('.overInfo img::attr(src)').get(),
                'features':  real_estate.css('div.characteristics div.item::text').getall(),
                'link': real_estate.css('a.anuncioLink::attr(href)').get(),
                'real_estate_agent': real_estate.xpath('./@data-is-from-especialista').get(),
                'remote_id': real_estate.xpath('./@id').get(),
                'operation': 'sale' if 'venta' in response.request.url else 'rent',
            }

        # next_page_url = response.css(
        #     'div.pager span.item.selected + a.item::attr(href)').get()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
