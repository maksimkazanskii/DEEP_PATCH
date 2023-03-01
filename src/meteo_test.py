from datetime import datetime
from meteostat import Normals,Point
import matplotlib.pyplot as plt
from meteostat import Stations, Monthly
from geopy.geocoders import Nominatim
import csv
# user name: maximkax,
# password:Geo2555"
stations = Stations()
stations = stations.nearby(42.3601,71.0589)
station = stations.fetch(1)


#data = Normals(station, None, None)
#list_of_places =["La Caleta, Dominican Republic",
#                 "Santiago, Chile",
#                 "South Andros, Sanctuary Blue Hole,	Bahamas",
#                 "Alaska, western interior, Tochak McGrath, Upper Kuskokwim River,	USA",
#                 "Abaco, Hopetown,	Bahamas",
#                 "Uelen Chukotka, Russia",
#                 "La Caleta,	Dominican Republic"]


#gn = geocoders.GeoNames(username= "maximkax")

location_csv = "../data/geo_locations/locations_test.csv"

list_of_places = []
with open(location_csv, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        list_of_places.append("".join(row))


for item in list_of_places:
    locator = Nominatim(user_agent="maximkax")
    location = locator.geocode(item)
    try:
        print("****")
        print(item, " Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        stations = stations.nearby(location.latitude, location.longitude)
        station = stations.fetch(1)

        start = datetime(2010, 1, 1)
        end = datetime(2015, 12, 31)
        data = Monthly(station, start, end)
        data = data.fetch()
        print("average temperature : ", data[['tavg']].mean())
        print("average precipitation : ", data[['prcp']].mean())
        data.plot(y=['tavg', 'prcp'])
        plt.show()
        print("****")
    except:
        print("WARNING : Location was not found",item)

