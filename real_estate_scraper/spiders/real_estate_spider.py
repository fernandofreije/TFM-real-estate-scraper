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

        to_scrap = self.settings["PROVINCES_TO_SCRAP"]

        logging.info(f'To scrap config -- {to_scrap}')
        if (to_scrap != 'all'):
            provinces = {key: value for key,
                         value in provinces.items() if key in to_scrap.split(',')}

        logging.info(f'Provinces to scrap - - {provinces.keys()}')

        for province, province_url_name in provinces.items():
            urls = [
                f'https://www.pisos.com/{operation}/pisos-{province_url_name}/fecharecientedesde-desc/' for operation in ['venta', 'alquiler']
            ]

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, meta={'province': province})

    def parse(self, response):
        logging.info(f'Parsing page {response.request.url}')
        page = int(response.css('.pager .item.selected::text').get())
        position = 1
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
                'real_estate_agent': real_estate.css('img.anunciante-logo').get(),
                'remote_id': real_estate.xpath('./@id').get(),
                'operation': 'sale' if 'venta' in response.request.url else 'rent',
                'province': response.meta['province'],
                'page-position': f'{page:03d}-{position:02d}'
            }
            position += 1

        next_page_url = response.css(
            'div.pager span.item.selected + a.item::attr(href)').get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), meta={'province': response.meta['province']})
