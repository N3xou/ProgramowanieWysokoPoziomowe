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

