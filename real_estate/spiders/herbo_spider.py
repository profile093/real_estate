import scrapy
from real_estate.items import RealEstateItem

class HerboSpider(scrapy.Spider):
    name = 'herbo'
    allowed_domains = ['herbo.se']
    start_urls = ['https://bostad.herbo.se']

    def parse(self, response):
        for property in response.css('div.property'):
            item = RealEstateItem()
            item['url'] = response.urljoin(property.css('a::attr(href)').get())
            item['title'] = property.css('h4.title::text').get()
            item['status'] = property.css('span.status::text').get()
            item['pictures'] = property.css('img::attr(src)').getall()
            item['rent_price'] = self.parse_price(property.css('span.price::text').get())
            item['description'] = property.css('div.description::text').get()
            item['phone_number'] = property.css('span.phone::text').get()
            item['email'] = property.css('a[href^="mailto:"]::text').get()
            yield item

    def parse_price(self, price):
        if price:
            price = price.replace('kr', '').replace(',', '').strip()
            return float(price)
        return None
