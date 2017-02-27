"""

Author: Henry Ollarves
Date: 02/21/2017

Movie Trailer website project.

"""

import MovieDb
import Media
import fresh_tomatoes

def Main():

    # Main function that runs the program

    print('Running...')

    # Get movies
    movies = MovieDb.getPopularMovies()
    movies_data = []
    if(movies):
        # Fetching the first 10 movies
        for movie in movies[:10]:
            # Creating youtube link
            movie_video = MovieDb.getMovieTrailer(movie["id"])
            if(movie_video is not None):
                movie_youtube_key = movie_video["key"]
                video_url = "https://www.youtube.com/watch?v=" + movie_youtube_key
            poster_url = "http://image.tmdb.org/t/p/w342/" + movie["poster_path"]
            # Creating class instance
            object_data = Media.Movie(movie["title"], movie["overview"], video_url, poster_url, str(movie["vote_average"]))
            # Appending to array
            movies_data.append(object_data)

    # Get series
    series = MovieDb.getPopularSeries()
    series_data = []
    if(series):
        # Fetching the first 10 series
        for show in series[:10]:
            # Creating youtube link
            serie_video = MovieDb.getShowTrailer(show["id"])
            if(serie_video is not None):
                serie_youtube_key = serie_video["key"]
                video_url = "https://www.youtube.com/watch?v=" + serie_youtube_key
            poster_url = "http://image.tmdb.org/t/p/w342/" + show["poster_path"]
            # Creating class instance
            object_data = Media.Show(show["name"], show["overview"], video_url, poster_url, str(show["vote_average"]))
            # Appending to array
            series_data.append(object_data)

    # Pass on to fresh_tomatoes.py
    fresh_tomatoes.open_movies_page(movies_data, series_data)

# Running main function
Main()
