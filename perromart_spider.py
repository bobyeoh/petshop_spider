import requests
import json
import mongo


class Spider(object):
    def __init__(self):
        conn = mongo.get_mongo_db_client(
          mongo_url="mongodb://127.0.0.1:27017",
          max_pool_size=20
        )
        self.url = "https://perromart.com.sg/search?q=*&type=product&options%5Bprefix%5D=last&view=json"
        self.db = conn['perromart']
        self.start = False
        self.current_page = 0
        self.page_size = 10
        self.page_count = 0
        self.data_count = 0

    def getRawData(self):
        self.current_page += 1
        data = requests.get(self.url + "&page=" + str(self.current_page)).text
        data = json.loads(data)
        self.data_count = data['results_count']
        self.page_count = int(self.data_count / 10)
        if self.data_count % 10 != 0:
            self.page_count += 1
        return data['results']

    def run(self):
        while True:
            if self.current_page == self.page_count and self.start:
                print("Done")
                break
            self.start = True
            products = self.getRawData()
            for product in products:
                price = product['price']
                price = float(price.replace("$", ""))
                compare_at_price = product['compare_at_price']
                compare_at_price = float(compare_at_price.replace("$", ""))
                product['price'] = price
                product['compare_at_price'] = compare_at_price
                self.db['product'].insert_one(product)
            print("Current Page: " + str(self.current_page))


s = Spider()
s.run()
