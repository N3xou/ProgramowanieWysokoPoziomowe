import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import threading
import datetime
import matplotlib.pyplot as plt
class Product:
    def __init__(self, name, url='', current_price = 0.0):
        self.name = name
        self.url = url
        self.current_price = current_price
    def update_price(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('p', class_='price_color')
        if price_element:
            # Extract the price text and strip out any non-numeric characters
            price_text = price_element.text.strip()


            price_number = re.sub(r'[^\d.,]', '', price_text)  # Regex

            price_number = price_number.replace(',', '.')

            try:
                price = float(price_number)
                if '£' in price_text:
                    price *= 5
                elif 'PLN' in price_text:
                    pass
                elif 'USD' in price_text or '$' in price_text:
                    price *= 4
                elif 'EUR' in price_text or '€' in price_text:
                    price *= 4.4
                else:
                    print('Nie rozpoznano waluty')
                    price = 0

                self.current_price = price

                # For debugging: print the extracted price text
                print(f"Zaktualizowano cene produktu {self.name } do: {price} PLN")

            except ValueError:
                print(f"Wystąpił błąd w rozpoznaniu ceny: {price_text}")
        else:
            print("Nie odnaleziono ceny.")



class PriceMonitor:
    def __init__(self, products = []):
        self.products = products
    def add_product(self, name, url):
        product = Product(name,url)
        product.update_price()
        self.products.append(product)
        print('Pomyślnie dodano produkt.')
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
                print("Anulowanie.")
                return
            elif 1 <= choice <= len(matching_products):
                self.products.remove(matching_products[choice - 1])
                print(f"{matching_products[choice - 1].name} został usunięty.")
            else:
                print("Wybrano niepoprawną opcję.")
        except ValueError:
            print("Błąd wprowadzono inny znak niż cyfra.")
    def update_all_prices(self):
        if len(self.products) < 1:
            print('Nie odnaleziono produktów do zaktualizowania cen.')
        else:
            for product in self.products:
                product.update_price()

    def get_cheapest_product(self):
        if not self.products:
            print("Nie znaleziono żadnego produktu w bazie.")
            return None

        cheapest_product = min(self.products, key=lambda product: product.current_price)
        print(f"Najtańszy produkt to {cheapest_product.name} kosztujący {cheapest_product.current_price} PLN")
        return cheapest_product

    def save_prices(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for product in self.products:
                writer.writerow([product.name, product.current_price, product.url])

    def load_prices(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.products = []  # Clear any existing products
            for row in reader:
                name, price, url = row  # Expect each row to have name, price, and url
                product = Product(name=name, url=url, current_price=float(price))
                self.products.append(product)

    def display_all_products(self):
        if not self.products:
            print("Brak produktów na liście.")
        else:
            print("Lista produktów i ich cen:")
            for product in self.products:
                print(f"Produkt: {product.name}, Cena: {product.current_price}")
    def automatic_price_update(self, filename, interval=60):
        def update_task():
            while True:
                self.update_all_prices()
                self.append_prices_to_csv(filename)
                time.sleep(interval)
        update_thread  = threading.Thread(target=update_task, daemon=True)
        update_thread.start()

    import csv
    import datetime

    def append_prices_to_csv(self, filename):
        # Load existing data from CSV file if it exists
        existing_data = {}
        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    name, prices, timestamps, url = row[0], eval(row[1]), eval(row[2]), row[3]
                    existing_data[name] = (prices, timestamps, url)
        except FileNotFoundError:
            pass

        # Update prices for monitored products and add a new timestamp
        for product in self.products:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if product.name in existing_data:
                prices, timestamps, url = existing_data[product.name]
                prices.append(product.current_price)
                timestamps.append(timestamp)
                existing_data[product.name] = (prices, timestamps, product.url)
            else:
                existing_data[product.name] = ([product.current_price], [timestamp], product.url)

        # Write data back to CSV
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for name, (prices, timestamps, url) in existing_data.items():
                writer.writerow([name, prices, timestamps, url])

        print(f"Ceny zostały zaktualizowane w pliku: {filename}")

    def plot_price_trends(self, filename, combine = False):
        # Load data from CSV file
        products_data = {}
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name, prices, timestamps, url = row[0], eval(row[1]), eval(row[2]), row[3]
                products_data[name] = (prices, timestamps)

        # Plot each product's price trend
        if not combine:
            for name, (prices, timestamps) in products_data.items():
                plt.figure(figsize=(10, 5))
                plt.plot(timestamps, prices, marker='o', linestyle='-')
                plt.title(f'Ceny dla {name}')
                plt.xlabel('Data')
                plt.ylabel('Cena w PLN')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
        else:
            plt.figure(figsize=(12, 6))
            plt.title('Price Trends for All Monitored Products')
            plt.xlabel('Timestamp')
            plt.ylabel('Price (PLN)')

            # Plot each product's price trend in a different color
            for name, (prices, timestamps) in products_data.items():
                plt.plot(timestamps, prices, marker='o', linestyle='-', label=name)

            # Rotate timestamps for better readability
            plt.xticks(rotation=45)
            plt.legend(title="Products")  # Add a legend with product names
            plt.tight_layout()
            plt.show()


def main():
    #monitor = PriceMonitor()
    product1 = Product("A Light in the Attic",
                      "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    product2 = Product("Tipping the Velvet", "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html")
    product3 = Product("Soumission", "http://books.toscrape.com/catalogue/soumission_998/index.html")

    monitor = PriceMonitor(products=[product1, product2, product3])

    # Update prices for the initialized products

    monitor.update_all_prices()
    monitor.automatic_price_update(filename='ceny2.csv',interval=60)
    print("Witaj w systemie monitorowania cen!")

    while True:
        print("\n1. Dodaj produkt do monitorowania")
        print("2. Usuń produkt")
        print("3. Zaktualizuj ceny produktów")
        print("4. Znajdź najtańszy produkt")
        print("5. Zapisz ceny do pliku")
        print("6. Wczytaj ceny z pliku")
        print("7. Wyjdź")
        print("8. Wyświetl wszystkie produkty")
        print("9. Wyświetl wykres cen.")

        choice = input("Wybierz opcję: ")

        if choice == "1":
            name = input("Podaj nazwę produktu: ")
            url = input("Podaj URL produktu: ")
            monitor.add_product(name, url)
        elif choice == "2":
            name = input("Podaj nazwę produktu do usunięcia: ")
            monitor.remove_product(name)
        elif choice == "3":
            monitor.update_all_prices()
        elif choice == "4":
            monitor.get_cheapest_product()
        elif choice == "5":
            filename = input("Podaj nazwę pliku do zapisania cen (np. ceny.csv): ")
            monitor.save_prices(filename)
        elif choice == "6":
            filename = input("Podaj nazwę pliku do wczytania cen (np. ceny.csv): ")
            monitor.load_prices(filename)
        elif choice == "7":
            print("Zamykanie programu.")
            break
        elif choice == "8":
            monitor.display_all_products()
        elif choice == "9":
            filename = input("Podaj nazwe pliku csv z ktorego chcesz stworzyc wykres cenowy. ")
            comb = input("Czy wyswietlic wykres kazdego produktu osobno?\n[1]Tak \n[2]Nie ")
            if comb == 1:
                combbool = False
            else:
                combbool = True
            monitor.plot_price_trends(filename = filename, combine = combbool)
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()
