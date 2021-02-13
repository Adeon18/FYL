import folium
import haversine

from math import sin, asin, cos, sqrt
from geopy.geocoders import Nominatim

from manager import read_file

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


def load_map(year: int, user_location: tuple):
    '''
    Loads the map with the user location
    '''
    mapp = folium.Map(location=user_location)

    mapp.add_child(folium.Marker(location=user_location,
            popup="Your set location",
            icon=folium.Icon()))
    
    mapp.save(f'{year}_movies_map.html')


def find_all_movies(year: int) -> tuple:
    '''
    Finds all movies that were shot at a certain year. Also calls a
    function for reading the locations file

    Args:
        year: The year you want the movies to be
    
    Returns:
        needed_movies: A list with elements like: (Name, Location) of right
            year movies
    '''
    needed_movies = []
    movie_data = read_file()

    for movie in movie_data:
        try:
            movie = movie.split('\t')
            # This horrific thing just returns the year from movie
            movie_year = movie[0].split('(')[1].split(')')[0]
            if int(movie_year) == year:
                needed_movies.append((movie[0], movie[-1] if  movie[-1][-1] != ')' else movie[-2]))
        except ValueError or IndexError:
            continue
    
    return needed_movies


def find_coords(movies: tuple) -> tuple:
    '''
    Gets the coords from a movie location

    Args:
        movies: The movie list returned from find_all_movies
    
    Returns:
        movies_coords: The same list as movies, but place is replaced with
            the (latitude, longtitude)
    
    >>> find_coords([('"#1 Single" (2006)', 'Los Angeles, California, USA')])
    [('"#1 Single" (2006)', (34.0536909, -118.242766))]
    '''
    movies_coords = []

    for movie in movies:

        location = None
        # Split the data
        movie_name, movie_place = movie[0], movie[1]
        movie_place = movie_place.split(',')
        # Define the geolocator with project_name
        geolocator = Nominatim(user_agent="FYL")

        # Get the place location in the most presise way possible
        start = 0
        while location == None:
            location = geolocator.geocode(movie_place[start:])
            start += 1
            if start == len(movie_place):
                break
        
        if location != None:
            movies_coords.append((movie_name, (location.latitude, location.longitude)))
        # Skip if there's any bad data
        continue

    return tuple(movies_coords)


def find_distance(user_position: tuple, places: tuple):
    '''
    Find distance between user coordinates and a given place
    '''
    distances = []
    for some_place in places:
        distance = haversine.haversine(user_position, some_place[1])

        distances.append((some_place[0], round(distance, 2), some_place[1]))
    
    return distances


def sort_distances(movies: tuple) -> tuple:

    #movies = list(movies).sort(key=lambda x:x[1])

    return sorted(list(movies), key = lambda x: x[1])[:10]



def combine():
    data = read_input()
    year, coords = data[0], data[1]

    return sort_distances(find_distance(coords, find_coords(find_all_movies(year))))






# def haversine_search(user_position: tuple, some_place: tuple):
#     radius = 6356.752 / 4
#     distance = 2 * radius *\
#                asin(sqrt((sin((some_place[0] - user_position[0]) / 2) ** 2) +\
#                cos(user_position[0]) * cos(some_place[0]) *\
#                sin((some_place[1] - user_position[1]) / 2) ** 2))
    
#     return distance


if __name__ == '__main__':
    # print(sort_distances(find_distance((34.0536909, -118.242766), find_coords(find_all_movies(2015)))))
    # import doctest
    print(combine())
    # print(doctest.testmod())
    #movies_2015 = find_all_movies(2015)
    # print(movies_2015)
   # print(find_coords(movies_2015))
    #print(find_all_movies(2006))
