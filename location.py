import csv
from geopy.geocoders import Nominatim

MAX_SQRD_RADIUS = 0.000004


class Geolocator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent='why')

    def get_nearest(self, message):
        if message.location is not None:
            nearest = []
            long = message.location.longitude
            lat = message.location.latitude
            with open('./buildings_data/buildings.csv') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    x_dif = float(row['X']) - long
                    y_dif = float(row['Y']) - lat
                    sqrd_distance = x_dif*x_dif+y_dif*y_dif
                    if sqrd_distance < MAX_SQRD_RADIUS:
                        nearest.append(
                            {'name':
                             row['Название объекта культурного наследия'],
                             'address': row['Адрес'],
                             'history': row['История'],
                             'sqrd_distance': sqrd_distance})
            nearest.sort(key=lambda x: x['sqrd_distance'])
            del nearest[5:len(nearest)]
            return nearest
