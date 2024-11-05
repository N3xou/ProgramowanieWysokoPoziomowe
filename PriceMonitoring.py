import requests
class Product:
    def __init__(self, name, url, current_price = 0):
        self.name = name
        self.url = url
        self.current_price = current_price
    def update_price(self):
        response = requests.get(self.url)

        pass
class PriceMonitor:
    def __init__(self, products = []):
        self.products = products
    def add_product(self, name, url):
        product = Product(name,url)
        product.update_price()
        self.products.append(product)
    def remove_product(self, name):
        pass
    def update_all_prices(self):
        for product in self.products:
            product.update_price()
    def get_cheapest_product(self):
        pass
    def save_prices(self, filename):
        pass
    def load_prices(self, filename):
        pass


