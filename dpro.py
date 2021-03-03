from sys import argv, exit, float_info 
import csv
from math import sin, cos, sqrt, atan2, radians
import statistics


def find_city_for_station(station_name, cities_to_stations):
  # print("finding city for " + station_name)
  for city in cities_to_stations:
    # print(city)
    if station_name in cities_to_stations[city]:
      # print("city found " + city)
      return city

def calculate_weather(for_date, cities_to_stations):

  read_columns = ["STATION_NAME", "MEAN_TEMPERATURE", "LOCAL_YEAR", "LOCAL_MONTH", "LOCAL_DAY"]
  climate_csv = 'climate.csv'

  with open(climate_csv) as csvFile:
    reader = csv.DictReader(csvFile)

    climate_by_cities = {}
    for row in reader:
      station = row[read_columns[0]]
      temperature = row[read_columns[1]]
      temperature = float(temperature) if temperature else 0.0
      year = row[read_columns[2]]
      month = row[read_columns[3]]
      day = row[read_columns[4]]
      city = find_city_for_station(station, cities_to_stations)
      row_date = year + '-' + month + '-' + day

      if(for_date == row_date):
        if(city in climate_by_cities):
          city_data = climate_by_cities[city].append(temperature)
        else:
          temperatures = []
          temperatures.append(temperature)
          climate_by_cities[city] = temperatures
    
    for city in climate_by_cities:
      mean_temp = statistics.mean(climate_by_cities[city])
      median_temp = statistics.median(climate_by_cities[city])
      print("City: " + city + ", Mean weather: " + str(mean_temp if mean_temp else '') + ", Median weather: " + str(median_temp if median_temp else ''))
      # print("City: " + city + ", Median weather: " + str(median_temp if median_temp else ''))

# Compute distance between two coordinates in kms
# from: https://stackoverflow.com/a/19412565
def computeDistance(str_lat1, str_lon1, str_lat2, str_lon2):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(float(str_lat1))
    lon1 = radians(float(str_lon1))
    lat2 = radians(float(str_lat2))
    lon2 = radians(float(str_lon2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

if __name__ == '__main__':
    input_date = argv[1]
    cities_data_path = './cities.csv'
    climate_data_path = './climate.csv'
    city_to_coordinates = dict()
    station_to_coordinates = dict()
    cities_to_stations = dict()

    with open(cities_data_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for document_id, row in enumerate(csv_reader):
            city = row['city']
            lat = row['lat']
            lon = row['lng']
            coordinates = [lat, lon]
            city_to_coordinates[city] = coordinates
        # print(city_to_coordinates)

    with open(climate_data_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for document_id, row in enumerate(csv_reader):
            station_name = row['STATION_NAME']
            lat = row['lat']
            lon = row['lng']
            coordinates = [lat, lon]
            station_to_coordinates[station_name] = coordinates
        # print(station_to_coordinates)

    for station_name in station_to_coordinates:
        coordinates = station_to_coordinates[station_name]
        station_name_lat = coordinates[0]
        station_name_lon = coordinates[1]

        min_distance = float_info.max
        min_city = ""
        for city in city_to_coordinates:
            city_coordinates = city_to_coordinates[city]
            city_lat = city_coordinates[0]
            city_lon = city_coordinates[1]
            distance = computeDistance(station_name_lat, station_name_lon, city_lat, city_lon)
            if(distance < min_distance):
                min_distance = distance
                min_city = city
        if min_city in cities_to_stations:
            cities_to_stations[min_city].append(station_name)
        else:
            cities_to_stations[min_city] = [station_name]


    calculate_weather(input_date, cities_to_stations)