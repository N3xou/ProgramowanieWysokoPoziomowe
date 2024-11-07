import requests
from bs4 import BeautifulSoup
import csv
class Product:
    def __init__(self, name, url, current_price = 0):
        self.name = name
        self.url = url
        self.current_price = current_price
    def update_price(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('span', {'class': 'product-price'})
        if 'PLN' in price_element.text:
            price = float(price_element.text.replace(' PLN', '').replace(',', '.'))
        elif 'USD' or '$' in price_element.text:
            price = float(price_element.text.replace(' USD', '').replace(',', '.'))
            price = price * 4
        elif 'EUR' or '€' in price_element.text:
            price = float(price_element.text.replace(' EUR', '').replace(',', '.'))
            price = price * 4.4

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
        with open('ceny.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for product in self.products:
                writer.writerow([product.name, product.current_price])

    def load_prices(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            #self.products = []   # clearing products
            for row in reader:
                name, price = row
                product = Product(name, float(price))
                self.products.append(product)


z

