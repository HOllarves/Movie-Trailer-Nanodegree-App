import requests
import json
from Auth import ApiKey


"""

    Module to communicate with TheMovieDB RESTful API

"""

# Global vars
api_key = ApiKey()
api_movies_url = "https://api.themoviedb.org/3/movie/"
api_series_url = "https://api.themoviedb.org/3/tv/"

def getPopularMovies():

    # Fetchs popular movies from The Movie DB RESTful API

    popular_movies_url = api_movies_url + "popular?api_key=" + api_key +  "&language=en-US&page=1"
    # Making HTTP GET request
    r = requests.get(popular_movies_url)
    r.raise_for_status()
    # Decoding results
    data = json.loads(r.content.decode('utf-8'))
    return data["results"]

def getMovieTrailer(movie_id):

    # Get trailer of certain movie using The Movie DB RESTful API

    video_url = api_movies_url + str(movie_id) + "/videos?api_key=" + api_key
    # Making HTTP GET request
    r = requests.get(video_url)
    r.raise_for_status()
    # Decoding results
    data = json.loads(r.content.decode('utf-8'))
    if(len(data["results"]) > 0):
        return data["results"][0]
    else:
        return None

def getPopularSeries():

    # Fetchs popular series from The Movie DB RESTful API

    series_url = api_series_url + "popular?api_key=" + api_key + "&languange=en-US&page=1"
    # Making HTTP GET request
    r = requests.get(series_url)
    r.raise_for_status
    # Decoding results
    data = json.loads(r.content.decode('utf-8'))
    return data["results"]

def getShowTrailer(serie_id):

    # Get trailer of a certain show using The Movie DB RESTful API

    video_url = api_series_url + str(serie_id) + "/videos?api_key=" + api_key
    # Making HTTP GET request
    r = requests.get(video_url)
    r.raise_for_status()
    # Decoding results
    data = json.loads(r.content.decode('utf-8'))
    if(len(data["results"]) > 0):
        return data["results"][0]
    else:
        return None
