from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="FYL")
location = geolocator.geocode("Cold Spring, New York, USA")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)