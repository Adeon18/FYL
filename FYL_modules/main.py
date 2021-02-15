'''
The main script which also contains input management and map_generation
'''
import folium
from folium.plugins import MarkerCluster

from calculations import *


def read_input() -> tuple():
    '''
    Read the user input and check for input correction.

    Returns:
        A tuple with all of the data
    '''
    try:
        year = int(input("Please enter a year you would like to have a map for: "))
        latitude, longtitude = tuple(input("Please enter YOUR location (format: lat, long): ").split(', '))
        option = input('Type "speed" or "precision" depending which you want most(speed - very quick but not precise, precision - VERY slow but presice): ')

        return (year, (float(latitude), float(longtitude)), option)
    except ValueError:
        print("Wrong format, try again")


def load_map(year: int, user_location: tuple, closest_10: list):
    '''
    Loads the map with the user location.

    Args:
        year: User year
        user_location: User coordinates
        closest_10: Closest 10 movies
    
    Returns:
        Map name and saves the map with all of the data
    '''
    mapp = folium.Map(location=user_location)

    loc_fg = folium.FeatureGroup(name="Locations")
    wrld_fg = folium.FeatureGroup(name="Population")
    # location_fg = folium.FeatureGroup(name="Locations")
    marker_cluster = folium.plugins.MarkerCluster().add_to(loc_fg)

    loc_fg.add_child(folium.CircleMarker(location=user_location,
                popup="Your set location",
                icon=folium.Icon(), 
                fill_color='red',
                color='red',
                fill_opacity=1))
    
    for loctn in closest_10:
        popup = loctn[0]
        folium.Marker(location=loctn[2], popup=popup).add_to(marker_cluster)
    
    # Code taken from cms
    wrld_fg.add_child(folium.GeoJson(data=open('data/world.json', 'r',
        encoding='utf-8-sig').read(),
        style_function=lambda x: {'fillColor':'green'
        if x['properties']['POP2005'] < 10000000
        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
        else 'red'}))

    mapp.add_child(loc_fg)
    mapp.add_child(wrld_fg)
    mapp.add_child(folium.LayerControl())
    mapp.save(f'{year}_movies_map.html')

    return f'{year}_movies_map.html'


def main():
    '''
    The main function which unites everything
    '''
    data = read_input()
    year, coords, opt = data[0], data[1], data[2]
    if opt == 'speed':
        closest_10 = sort_distances(find_distance(coords, find_coords(sort_by_country(coords, find_all_movies(year)), opt)))
    elif opt == 'precision':
        closest_10 = sort_distances(find_distance(coords, find_coords(find_all_movies(year), opt)))
    else:
        print("Wrong input")
        return
    # print(closest_10)
    map_name = load_map(year, coords, closest_10)
    print(f"Finished, look at {map_name}")


main()
