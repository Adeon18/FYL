import folium
import pandas
data = pandas.read_csv("Stan_1900.csv")
lat = data['lat']
lon = data['lon']
churches = data['церкви']
hc = data['гр-кат.']
def color_creator(population):
    if population < 2000:
        return "green"
    elif 2000 <= population <= 3500:
        return "yellow"
    else:
        return "red"
map_ = folium.Map(location=[48.314775, 25.082925],
 zoom_start=10)
fg = folium.FeatureGroup(name="Kosiv_map")
for lt, ln, ch, hc in zip(lat, lon, churches, hc):
    fg.add_child(folium.CircleMarker(location=[lt, ln],
        radius=10,
        popup="1900 рік"+"\n" + ch,
        fill_color=color_creator(hc),
        color='red',
        fill_opacity=0.5))
map_.add_child(fg)
map_.save('Map_6.html')