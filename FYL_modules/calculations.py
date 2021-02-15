"""
Module for managing all the calculations regarding distance and coordinates.
Also optimisation is here
"""
import time
import sys
import random
import haversine
import progressbar

from math import sin, asin, cos, sqrt
from geopy.geocoders import Nominatim

from manager import read_file


def find_all_movies(year: int) -> tuple:
    """
    Finds all movies that were shot at a certain year. Also calls a
    function for reading the locations file

    Args:
        year: The year you want the movies to be

    Returns:
        needed_movies: A list with elements like: (Name, Location) of right
            year movies
    """
    print("Starting year sync..", flush=True)
    start = time.time()

    needed_movies = []
    movie_data = read_file()

    for movie in movie_data:
        try:
            movie = movie.split("\t")
            # This horrific thing just returns the year from movie
            movie_year = movie[0].split("(")[1].split(")")[0]
            if int(movie_year) == year:
                needed_movies.append(
                    (movie[0], movie[-1] if movie[-1][-1] != ")" else movie[-2])
                )
        except (ValueError, IndexError):
            continue

    print(f"Ended year sync in {round(time.time() - start, 3)} sec", flush=True)
    return needed_movies


def sort_by_country(user_pos: tuple, movies: tuple) -> tuple:
    """
    Sorts by contry for speed purposes. Is not used for precision.

    Args:
        user_pos: User coordinates
        movies: movie list from find_all_movies

    Returns:
        needed_movies: A list with elements like: (Name, Location) of right
            country movies
    """
    geolocator = Nominatim(user_agent="FYL")
    position = str(user_pos[0]) + ", " + str(user_pos[1])
    location = geolocator.reverse(position, language="en")
    location = str(location).split(",")

    if "United States" in location[-1]:
        location[-1] = "USA"

    needed_movies = []
    for movie in movies:
        movie_name, movie_place = movie[0], movie[1]
        # movie_place = movie_place.split(',')
        # print(location)
        # print(str(', '.join(location[-3:len(location):2])))
        if location[-1] in movie_place:
            needed_movies.append(movie)

    while len(needed_movies) < 11:
        try:
            needed_movies.append(movies[random.randrange(0, len(movies))])
        except ValueError:
            print("Please enter a valid year", flush=1)
            sys.exit()

    while len(needed_movies) > 400:
        needed_movies = random.choice(
            [
                needed_movies[: len(needed_movies) // 2],
                needed_movies[len(needed_movies) // 2 :],
            ]
        )

    return tuple(needed_movies)


def find_coords(movies: tuple, opt: str) -> tuple:
    """
    Gets the coords from a movie location

    Args:
        movies: The movie list returned from find_all_movies or sort_by_country
        opt: Presition parameter

    Returns:
        movies_coords: The same list as movies, but place is replaced with
            the (latitude, longtitude)

    >>> find_coords([('"#1 Single" (2006)', 'Los Angeles, California, USA')])
    [('"#1 Single" (2006)', (34.0536909, -118.242766))]
    """
    print(f"Finding coords.. for {len(movies)} elems", flush=True)
    start = time.time()

    bar = progressbar.ProgressBar(
        maxval=len(movies),
        widgets=[progressbar.Bar("=", "[", "]"), " ", progressbar.Percentage()],
    )

    movies_coords = []

    bar.start()
    for i, movie in enumerate(movies):

        location = None
        # Split the data
        movie_name, movie_place = movie[0], movie[1]
        movie_place = movie_place.split(",")
        # Define the geolocator with project_name
        geolocator = Nominatim(user_agent="FYL")

        if opt == "precision":
            # Get the place location in the most presise way possible
            start = 0
            while location == None:
                location = geolocator.geocode(movie_place[start:])
                start += 1
                if start == len(movie_place):
                    break
        else:
            location = geolocator.geocode(movie_place[-1])

        bar.update(i + 1)
        if location != None:
            # print(i/len(movies) * 100, flush=True)
            movies_coords.append((movie_name, (location.latitude, location.longitude)))
        else:
            # Skip if there's any bad data
            continue
    bar.finish()
    print(f"Found coords in {round(time.time() - start, 3)} sec", flush=True)

    return tuple(movies_coords)


def find_distance(user_position: tuple, places: tuple) -> list:
    """
    Find distance between user coordinates and a given place.

    Args:
        user_position: User coordinates
        places: movie list from find_coords

    Returns:
        distances: list with (Name, distance, coordinates) as elements
    """
    print("Finding distance..", flush=True)
    start = time.time()

    distances = []
    for some_place in places:
        distance = haversine.haversine(user_position, some_place[1])

        distances.append((some_place[0], round(distance, 2), some_place[1]))

    print(f"Found distance in {round(time.time() - start, 3)} sec", flush=True)
    return distances


def sort_distances(movies: tuple) -> list:
    """
    Sorts the distances to get the best 10.

    Args:
        movies: movie_list from find_distance

    Returns:
        Sorted list
    """
    print("Sorting..", flush=True)
    start = time.time()

    print(f"Sorted in {round(time.time() - start, 3)} sec", flush=True)
    return sorted(list(movies), key=lambda x: x[1])[:10]


if __name__ == "__main__":
    pass
