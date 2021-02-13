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

map_= folium.Map(location=[48.314775, 25.082925],
 zoom_start=10)
fg_hc = folium.FeatureGroup(name="Greek Catholic")
for lt, ln, ch, hc in zip(lat, lon, churches, hc):
    fg_hc.add_child(folium.CircleMarker(location=[lt, ln],
    radius=10,
    popup="1900 рік"+"\n" + ch,
    fill_color=color_creator(hc),
    color='red',
    fill_opacity=0.5))

fg_pp = folium.FeatureGroup(name="Population")

fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                encoding='utf-8-sig').read(),
                style_function=lambda x: {'fillColor':'green'
                if x['properties']['POP2005'] < 10000000
                else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                else 'red'}))
map_.add_child(fg_hc)
map_.add_child(fg_pp)
map_.add_child(folium.LayerControl())
map_.save('Map_7.html')