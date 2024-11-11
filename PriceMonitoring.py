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
        matching_products = [product for product in self.products if name.lower() in product.name.lower()]

        if not matching_products:
            print("Nie odnaleziono produktu.")
            return

        for i, product in enumerate(matching_products, start=1):
            print(f"{i}. {product.name} - Cena: {product.current_price} PLN")

        try:
            choice = int(input("Wybierz numer produktu do usunięcia lub wprowadz 0 aby anyluwać.: "))
            if choice == 0:
                print("Operation cancelled.")
                return
            elif 1 <= choice <= len(matching_products):
                self.products.remove(matching_products[choice - 1])
                print(f"{matching_products[choice - 1].name} has been removed.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Operation cancelled.")
    def update_all_prices(self):
        for product in self.products:
            product.update_price()

    def get_cheapest_product(self):
        if not self.products:
            print("Nie znaleziono żadnego produktu w bazie.")
            return None

        cheapest_product = min(self.products, key=lambda product: product.current_price)
        print(f"The cheapest product is {cheapest_product.name} with a price of {cheapest_product.current_price} PLN")
        return cheapest_product
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


zb

