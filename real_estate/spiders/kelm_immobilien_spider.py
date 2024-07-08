import scrapy
from real_estate.items import RealEstateItem

class KelmImmobilienSpider(scrapy.Spider):
    name = 'kelm_immobilien'
    allowed_domains = ['kelm-immobilien.de']
    start_urls = ['https://kelm-immobilien.de/immobilien']

    def parse(self, response):
        properties = response.xpath('//div[contains(@class, "property-container")]')
        self.log(f'Found {len(properties)} properties')
        for property in properties:
            item = RealEstateItem()
            item['url'] = response.urljoin(property.xpath('.//a[@class="thumbnail"]/@href').get())
            item['title'] = property.xpath('.//h3[@class="property-title"]/a/text()').get()
            item['status'] = property.xpath('.//div[@class="property-subtitle"]/text()').get()
            item['pictures'] = property.xpath('.//a[@class="thumbnail"]/img/@src').getall()
            # Переход на страницу объявления
            request = scrapy.Request(url=item['url'], callback=self.parse_property)
            request.meta['item'] = item
            yield request

        # Пагинация
        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_property(self, response):
        item = response.meta['item']
        # Попробуем другой подход для извлечения цены
        kaufpreis_text = response.xpath('//div[contains(@class, "data-kaufpreis")]/div[contains(@class, "dd")]/text()').get()
        self.log(f'Found kaufpreis text: {kaufpreis_text}')  # Отладочное сообщение
        if kaufpreis_text:
            # Удаляем пробелы, заменяем запятые и точки, конвертируем в float
            kaufpreis_clean = kaufpreis_text.strip().replace('\u202f', '').replace(' EUR', '').replace('.', '').replace(',', '.')
            try:
                item['rent_price'] = float(kaufpreis_clean)
                self.log(f'Parsed rent price: {item["rent_price"]}')  # Отладочное сообщение
            except ValueError:
                item['rent_price'] = None  # Если не удается преобразовать в float
                self.log('Failed to convert kaufpreis to float')  # Отладочное сообщение
        else:
            item['rent_price'] = None  # Если не найдено
            self.log('No kaufpreis text found')  # Отладочное сообщение
        item['description'] = ' '.join(response.xpath('//div[@class="property-description"]/p/text()').getall()).strip()
        item['phone_number'] = response.xpath('//a[contains(@href, "tel:")]/text()').get()
        item['email'] = response.xpath('//a[contains(@href, "mailto:")]/text()').get()
        self.log(f'Scraped property details: {item}')
        yield item
