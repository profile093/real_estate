import json

class RealEstatePipeline:
    def open_spider(self, spider):
        self.data = {"Country": {"Germany": {"Domain": {"kelm-immobilien.de": []}}}}

    def close_spider(self, spider):
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        rental_object = {
            "url": item.get('url'),
            "title": item.get('title'),
            "status": item.get('status'),
            "pictures": item.get('pictures'),
            "rent_price": item.get('rent_price'),
            "description": item.get('description'),
            "phone_number": item.get('phone_number'),
            "email": item.get('email')
        }
        self.data["Country"]["Germany"]["Domain"]["kelm-immobilien.de"].append(rental_object)
        return item
