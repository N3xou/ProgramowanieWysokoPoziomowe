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

    def get_temperatures(self, location: str):
        return self.matrix.get(location, np.array([]))

    def get_average_temperature(self, location: str):
        temperatures = self.get_temperatures(location)
        if temperatures.size == 0:
            return None  # Brak danych dla podanej lokalizacji
        return np.mean(temperatures)

    def get_all_locations(self):
        return list(self.matrix.keys())

    def __str__(self):
        result = ""
        for location, temperatures in self.matrix.items():
            result += f"Lokalizacja: {location}, Temperatury: {temperatures}\n"
        return result