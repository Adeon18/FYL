import folium

from calculations import *


def read_input():
    '''
    Read the user input and check for input correction
    '''
    try:
        year = int(input("Please enter a year you would like to have a map for: "))
        latitude, longtitude = tuple(input("Please enter your location (format: lat, long): ").split(', '))

        return (year, (float(latitude), float(longtitude)))
    except ValueError:
        print("Wrong format, try again")


def load_map(year: int, user_location: tuple, closest_10: list):
    '''
    Loads the map with the user location
    '''
    mapp = folium.Map(location=user_location)

    user_fg = folium.FeatureGroup(name="User")
    location_fg = folium.FeatureGroup(name="Locations")

    user_fg.add_child(folium.CircleMarker(location=user_location,
                popup="Your set location",
                icon=folium.Icon(), 
                fill_color='red',
                color='red',
                fill_opacity=1))
    
    for loctn in closest_10:
        location_fg.add_child(folium.Marker(location=loctn[2],
        popup=loctn[0],
        icon=folium.Icon()))
    
    mapp.add_child(user_fg)
    mapp.add_child(location_fg)
    mapp.add_child(folium.LayerControl())
    mapp.save(f'{year}_movies_map.html')


def combine():
    data = read_input()
    year, coords = data[0], data[1]

    closest_10 = sort_distances(find_distance(coords, find_coords(find_all_movies(year))))
    # print(closest_10)
    load_map(year, coords, closest_10)

combine()
