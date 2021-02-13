import folium
import pandas
data = pandas.read_csv("Stan_1900.csv", error_bad_lines=False)
lat = data['lat']
lon = data['lon']
map_ = folium.Map(location=[48.314775, 25.082925],
 zoom_start=10)
fg = folium.FeatureGroup(name="Kosiv map")

churches = data['церкви']

for lt, ln, ch in zip(lat, lon, churches):
    fg.add_child(folium.Marker(location=[lt, ln],
    popup="1900 рік"+ ch,
    icon=folium.Icon()))
map_.add_child(fg)
map_.save('Map_5.html')