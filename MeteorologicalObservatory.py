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
        # Słowniki, gdzie klucze to lokalizacje, a wartości temp/wilgotnosc/cisnienie
        self.temperature_matrix = {}
        self.humidity_matrix = {}
        self.pressure_matrix = {}

    def add_measurements(self, location: str, temperatures: list, pressures: list = None, humidities: list = None):
        if location in self.temperature_matrix:
            self.temperature_matrix[location] = np.append(self.temperature_matrix[location], temperatures)
        else:
            self.temperature_matrix[location] = np.array(temperatures)

        if humidities is not None:
            if location in self.humidity_matrix:
                self.humidity_matrix[location] = np.append(self.humidity_matrix[location], humidities)
            else:
                self.humidity_matrix[location] = np.array(humidities)

        if pressures is not None:
            if location in self.pressure_matrix:
                self.pressure_matrix[location] = np.append(self.pressure_matrix[location], pressures)
            else:
                self.pressure_matrix[location] = np.array(pressures)

    def get_mean_temperature(self, location: str):

        temperatures = self.temperature_matrix.get(location, np.array([]))
        if temperatures.size == 0:
            print('Brak danych dla lokalizacji')
            return None
        return np.mean(temperatures)


    def get_average_per_day(self):
        # Calculate average for all parameters and display them
        max_length = max(len(temps) for temps in self.temperature_matrix.values())

        averages = {
            "temperature": [],
            "humidity": [],
            "pressure": []
        }

        # Calculate padded averages for temperature
        for temperatures in self.temperature_matrix.values():
            mean_value = np.mean(temperatures)
            padded = np.pad(temperatures, (0, max_length - len(temperatures)), constant_values=mean_value)
            averages["temperature"].append(padded)

        # Calculate padded averages for humidity
        for humidities in self.humidity_matrix.values():
            mean_value = np.mean(humidities) if humidities.size > 0 else 0
            padded = np.pad(humidities, (0, max_length - len(humidities)), constant_values=mean_value)
            averages["humidity"].append(padded)

        # Calculate padded averages for pressure
        for pressures in self.pressure_matrix.values():
            mean_value = np.mean(pressures) if pressures.size > 0 else 0
            padded = np.pad(pressures, (0, max_length - len(pressures)), constant_values=mean_value)
            averages["pressure"].append(padded)

        # Calculate final averages for each index
        avg_temperature = np.average(averages["temperature"], axis=0)
        avg_humidity = np.average(averages["humidity"], axis=0)
        avg_pressure = np.average(averages["pressure"], axis=0)

        return {
            "average_temperature": avg_temperature.tolist(),
            "average_humidity": avg_humidity.tolist(),
            "average_pressure": avg_pressure.tolist()
        }

    def get_max_temperature(self):
        max_temp = None
        for temperatures in self.temperature_matrix.values():
            if temperatures.size > 0:
                current_max = np.max(temperatures)
                if max_temp is None or current_max > max_temp:
                    max_temp = current_max
        return max_temp

    def get_all_locations(self):
        return list(self.temperature_matrix.keys())

    def __str__(self):
        result = "Temperature Matrix:\n"
        for location, temperatures in self.temperature_matrix.items():
            result += f"Lokalizacja: {location}, Temperatury: {temperatures}\n"

        result += "\nHumidity Matrix:\n"
        for location, humidities in self.humidity_matrix.items():
            result += f"Lokalizacja: {location}, Wilgotność: {humidities}\n"

        result += "\nPressure Matrix:\n"
        for location, pressures in self.pressure_matrix.items():
            result += f"Lokalizacja: {location}, Ciśnienie: {pressures}\n"

        return result


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
        self.temperature_matrix.add_measurements("Kraków", [13,16,14.2,13,9.2,8.2], [1011,1014,1011, 1021,1014])
        self.temperature_matrix.add_measurements('Gdańsk', [7.2,8.3,11.2], humidities=[11,15,16])
        self.temperature_matrix.add_measurements('Gdańsk', [7.2, 8.3, 11.2],[1000,999,700],[12,14,16])
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
                    print("[1] Dodaj wiele danych dla lokalizacji.")
                    print("[2] Oblicz średnie wartości dla wszystkich lokalizacji.")
                    print("[3] Wyświetl maksymalną temperaturę.")
                    print("[4] Cofnij")
                    sub_option = int(input("Wybierz opcję: "))


                    if sub_option == 1:
                        location = input("Podaj lokalizację: ")
                        temperature = list(map(float, input("Podaj temperatury oddzielone spacją: ").split()))
                        pressure = list(map(float, input("Podaj ciśnienie oddzielone spacją: ").split()))
                        humidity = list(map(float, input("Podaj wilgotność oddzielone spacją: ").split()))
                        self.temperature_matrix.add_measurements(location, temperature,pressure,humidity)
                        print("Dodano pomiary dla lokalizacji.\n")



                    elif sub_option == 2:

                        # Get the average values for temperature, humidity, and pressure

                        averages = self.temperature_matrix.get_average_per_day()  # Adjust method call

                        if averages is not None:

                            print("Średnie wartości dzienne (dla wszystkich lokalizacji):")

                            # Display average temperature

                            print("\nŚrednia temperatura:")

                            for i, temp in enumerate(averages['average_temperature'], 1):
                                print(f"Dzień {i}: {temp:.2f}°C")

                            # Display average humidity

                            print("\nŚrednia wilgotność:")

                            for i, humidity in enumerate(averages['average_humidity'], 1):
                                print(f"Dzień {i}: {humidity:.2f}%")

                            # Display average pressure

                            print("\nŚrednie ciśnienie:")

                            for i, pressure in enumerate(averages['average_pressure'], 1):
                                print(f"Dzień {i}: {pressure:.2f} hPa")

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
