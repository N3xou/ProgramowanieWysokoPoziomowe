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

