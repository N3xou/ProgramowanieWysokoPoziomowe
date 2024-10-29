import numpy as np
import pandas as pd
from datetime import datetime
class Measurement:
    def __init__(self, location , datetime ,value):
        self.location = location
        self.datetime = datetime
        self.value = value
    def __str__(self):
        return f'Lokalizacja: {self.location}, data: {self.datetime}, wartość pomiaru: {self.value}'
class WeatherData:
    def __init__(self, measurements = []):
        self.measurements = measurements

    def __str__(self):
        return '\n'.join(str(measurement) for measurement in self.measurements)

    def add_measurement(self, location: str, datetime_str: str, value: float):
        measurement = Measurement(location, datetime_str, value)
        self.measurements.append(measurement)

    def get_measurements_by_location(self, location: str):

        return [measurement for measurement in self.measurements if location.lower() in measurement.location.lower()]

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
        self.measurements = []
        with open(filename, 'r') as file:
            for line in file:
                location, datetime, value = line.strip().split(', ')
                self.add_measurement(location, datetime, float(value))

    def display_data_table(self):
        if not self.measurements:
            print("Brak danych do wyświetlenia.")
            return

        data = {
            "Lokalizacja": [m.location for m in self.measurements],
            "Data i godzina": [m.datetime for m in self.measurements],
            "Temperatura (°C)": [m.value for m in self.measurements]
        }

        # Create and display the DataFrame
        df = pd.DataFrame(data)
        print(df)

    def sort_measurements(self, by):

        if by == "temperature":
            self.measurements.sort(key=lambda m: m.value)
        elif by == "date":
            try:
                self.measurements.sort(key=lambda m: datetime.strptime(m.datetime, "%Y-%m-%d %H:%M"))
            except ValueError:
                print(
                    "Nieprawidłowy format daty w jednym z pomiarów. Upewnij się, że jest w formacie 'YYYY-MM-DD HH:MM'.")
        print('Dane zostały posortowane.')
class TemperatureMatrix:
    def __init__(self):
        self.matrix = {}  # Słownik, gdzie klucze to lokalizacje, a wartości to wektory temperatur (NumPy)

    def add_measurements(self, location: str, values: list):
        if location in self.matrix:
            self.matrix[location] = np.append(self.matrix[location], values)
        else:
            self.matrix[location] = np.array(values)

    def get_mean_temperature(self, location: str):

        temperatures = self.matrix.get(location, np.array([]))
        if temperatures.size == 0:
            print('Brak danych dla lokalizacji')
            return None
        return np.mean(temperatures)

    def get_average_per_day(self):
        max_length = max(len(temps) for temps in self.matrix.values())
        padded_temps = []
        for temperatures in self.matrix.values():
            mean_value = np.mean(temperatures)
            padded = np.pad(temperatures, (0, max_length - len(temperatures)), constant_values=mean_value)
            padded_temps.append(padded)

        average_per_index = np.average(padded_temps, axis=0)
        return average_per_index.tolist()

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
temperature_matrix.add_measurements("Warszawa", [15.5,13.1,17])
temperature_matrix.add_measurements("Opole", [17.3,1.2,14])
temperature_matrix.add_measurements("Kraków", [14.0,11,35])

class WeatherApp:
    def __init__(self):
        self.weather_data = WeatherData()
        self.temperature_matrix = TemperatureMatrix()

    def run(self):
        exit_program = False
        self.weather_data.add_measurement("Warszawa", "2024-10-20 12:00", 15.2)
        self.weather_data.add_measurement("Kraków", "2024-10-21 14:00", 13.5)
        self.weather_data.add_measurement("Gdańsk", "2024-10-22 09:30", 16.8)
        self.temperature_matrix.add_measurements("Warszawa", [11,14,13.5,12,11])
        self.temperature_matrix.add_measurements("Kraków", [13,16,14.2,13,9.2,8.2])
        self.temperature_matrix.add_measurements('Gdańsk', [7.2,8.3,11.2])
        while not exit_program:
            print("Witaj w aplikacji pogodowej! Wybierz jedną z opcji:")
            print("[1] Dodaj nowy pomiar.")
            print("[2] Wyświetl pomiary dla wybranej lokalizacji.")
            print("[3] Oblicz średnią temperaturę dla wybranej lokalizacji.")
            print("[4] Zapisz dane do pliku.")
            print("[5] Wczytaj dane z pliku.")
            print("[6] Analiza danych w formie macierzy.")
            print("[7] Wyświetl dane w postaci tabeli.")
            print("[8] Posortuj dane")
            print("[9] Wyjdź z programu.")
            option = int(input("Wprowadź swój wybór: "))

            if option == 1:
                location = input("Podaj lokalizację: ")
                datetime = input("Podaj datę i godzinę pomiaru (format: YYYY-MM-DD HH:MM): ")
                value = float(input("Podaj wartość temperatury: "))
                self.weather_data.add_measurement(location, datetime, value)
                print("Dodano nowy pomiar.\n")
            elif option == 2:
                location = input("Podaj lokalizację: ")
                measurements = self.weather_data.get_measurements_by_location(location)
                if measurements:
                    print(f"Pomiary dla lokalizacji {location}:")
                    for measurement in measurements:
                        print(measurement)
                else:
                    print("Brak pomiarów dla podanej lokalizacji.\n")

            elif option == 3:
                location = input("Podaj lokalizację: ")
                avg_temp = self.weather_data.get_average_temperature(location)
                if avg_temp is not None:
                    print(f"Średnia temperatura dla lokalizacji {location}: {avg_temp:.2f}°C\n")
                else:
                    print("Brak danych dla podanej lokalizacji.\n")

            elif option == 4:
                filename = input("Podaj nazwę pliku do zapisu: ")
                self.weather_data.save_to_file(filename)
                print(f"Dane zapisano do pliku {filename}.\n")

            elif option == 5:
                filename = input("Podaj nazwę pliku do odczytu: ")
                self.weather_data.load_from_file(filename)
                print(f"Dane wczytano z pliku {filename}.\n")

            elif option == 6:
                exit_sub = False
                while not exit_sub:
                    print("Opcje analizy danych:")
                    print("[1] Dodaj wyniki dla wielu lokalizacji.")
                    print("[2] Oblicz średnią temperaturę dla wszystkich lokalizacji.")
                    print("[3] Wyświetl maksymalną temperaturę.")
                    print("[4] Cofnij")
                    sub_option = int(input("Wybierz opcję: "))


                    if sub_option == 1:
                        location = input("Podaj lokalizację: ")
                        values = list(map(float, input("Podaj temperatury oddzielone spacją: ").split()))
                        self.temperature_matrix.add_measurements(location, values)
                        print("Dodano pomiary dla lokalizacji.\n")


                    elif sub_option == 2:

                        avg_temp = self.temperature_matrix.get_average_per_day()

                        if avg_temp is not None:

                            print("Średnia temperatura dzienna (dla wszystkich lokalizacji):")

                            for i, temp in enumerate(avg_temp, 1):
                                print(f"Dzień {i}: {temp:.2f}°C")

                            print()

                        else:

                            print("Brak danych do analizy.\n")

                    elif sub_option == 3:
                        max_temp = self.temperature_matrix.get_max_temperature()
                        if max_temp is not None:
                            print(f"Maksymalna zmierzona temperatura: {max_temp:.2f}°C\n")
                        else:
                            print("Brak danych do analizy.\n")
                    elif sub_option == 4:
                        exit_sub = True
                    else:
                        print("Wybrano niepoprawny numer, spróbuj ponownie.\n")
            elif option == 7:
                self.weather_data.display_data_table()
            elif option == 8:
                exit_sub = False
                while not exit_sub:
                    print("Opcje sortowania:")
                    print("[1] Posortuj według temperatury.")
                    print("[2] Posortuj według daty.")
                    print("[3] Cofnij")
                    sub_option = int(input("Wybierz opcję: "))
                    if sub_option == 1:
                        self.weather_data.sort_measurements("temperature")
                        exit_sub = True
                    elif sub_option == 2:
                        self.weather_data.sort_measurements("date")
                        exit_sub = True
                    elif sub_option == 3:
                        exit_sub = True
                    else:
                        print("Wybrano niepoprawny numer, spróbuj ponownie.\n")
            elif option == 9:
                exit_program = True
                print("Zakończono działanie programu. Do widzenia!")
            else:
                print("Wybrano niepoprawny numer, spróbuj jeszcze raz.\n")

app = WeatherApp()
app.run()
