import folium

#map_ = folium.Map(tiles="Stamen Terrain")

map_ = folium.Map(tiles="Stamen Terrain", location=[49.817545, 24.023932], zoom_start=17)

map_.add_child(folium.Marker(location=[49.817545, 24.023932],
              popup="Хіба я тут!",
              icon=folium.Icon()))

map_.save("ffff.html")