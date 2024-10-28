import numpy as np
class Measurement:
    def __init__(self, location , datetime,value):
        self.location = location
        self.datetime = datetime
        self.value = value
    def __str__(self):
        return f'Lokalizacja: {self.location}, data: {self.datetime}, wartość pomiaru: {self.value}'
class WeatherData:
    def __init__(self):
        self.measurements = []

    def __str__(self):
        return '\n'.join(str(measurement) for measurement in self.measurements)

    def add_measurement(self, location: str, datetime: str, value: float):
        measurement = Measurement(location, datetime, value)
        self.measurements.append(measurement)

    def get_measurements_by_location(self, location: str):
        return [measurement for measurement in self.measurements if measurement.location == location]

    def get_average_temperature(self, location: str):
        location_measurements = self.get_measurements_by_location(location)
        if not location_measurements:
            return None

        total_value = sum(measurement.value for measurement in location_measurements)
        return total_value / len(location_measurements)

    def save_to_file(self, filename: str):

        with open(filename, 'w') as file:
            for measurement in self.measurements:
                file.write(f"{measurement.location}, {measurement.datetime}, {measurement.value}\n")

    def load_from_file(self, filename: str):

        self.measurements = []  # Czyści istniejące pomiary przed wczytaniem
        with open(filename, 'r') as file:
            for line in file:
                location, datetime, value = line.strip().split(', ')
                self.add_measurement(location, datetime, float(value))
class TemperatureMatrix:
    def __init__(self):
        self.matrix = {}  # Słownik, gdzie klucze to lokalizacje, a wartości to wektory temperatur (NumPy)

    def add_measurement(self, location: str, temperature: float):

        if location in self.matrix:
            self.matrix[location] = np.append(self.matrix[location], temperature)
        else:
            self.matrix[location] = np.array([temperature])

    def add_measurements(self, location: str, values: list):

        if location in self.matrix:
            self.matrix[location] = np.append(self.matrix[location], values)
        else:
            self.matrix[location] = np.array(values)

    def get_temperatures(self, location: str):
        return self.matrix.get(location, np.array([]))

    def get_average_temperature(self, location: str):

        temperatures = self.get_temperatures(location)
        if temperatures.size == 0:
            return None  # Brak danych dla podanej lokalizacji
        return np.mean(temperatures)

    def get_average_per_day(self):

        all_temperatures = []
        for temperatures in self.matrix.values():
            all_temperatures.extend(temperatures)  # Łączy wszystkie temperatury
        if not all_temperatures:
            return None  # Brak danych
        return np.mean(all_temperatures)

    def get_max_temperature(self):
        max_temp = None
        for temperatures in self.matrix.values():
            if temperatures.size > 0:
                current_max = np.max(temperatures)
                if max_temp is None or current_max > max_temp:
                    max_temp = current_max
        return max_temp

    def get_all_locations(self):

        return list(self.matrix.keys())

    def __str__(self):

        result = ""
        for location, temperatures in self.matrix.items():
            result += f"Lokalizacja: {location}, Temperatury: {temperatures}\n"
        return result

temperature_matrix = TemperatureMatrix()
temperature_matrix.add_measurement("Warszawa", 15.5)
temperature_matrix.add_measurement("Warszawa", 17.3)
temperature_matrix.add_measurement("Kraków", 14.0)

class WeatherApp:
    def __init__(self):
        self.weather_data = WeatherData()
        self.temperature_matrix = TemperatureMatrix()

    def run(self):
        exit_program = False
        while not exit_program:
            print("Witaj w aplikacji pogodowej! Wybierz jedną z opcji:")
            print("[1] Dodaj nowy pomiar.")
            print("[2] Wyświetl pomiary dla wybranej lokalizacji.")
            print("[3] Oblicz średnią temperaturę dla wybranej lokalizacji.")
            print("[4] Zapisz dane do pliku.")
            print("[5] Wczytaj dane z pliku.")
            print("[6] Analiza danych w formie macierzy.")
            print("[7] Wyjdź z programu.")
            option = int(input("Wprowadź swój wybór: "))

            if option == 1:
                location = input("Podaj lokalizację: ")
                datetime = input("Podaj datę i godzinę pomiaru (format: YYYY-MM-DD HH:MM): ")
                value = float(input("Podaj wartość temperatury: "))
                self.weather_data.add_measurement(location, datetime, value)
                self.temperature_matrix.add_measurement(location, value)
                print("Dodano nowy pomiar.\n")