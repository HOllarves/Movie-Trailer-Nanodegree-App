import webbrowser
import os
import inspect
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        @font-face {
            font-family: OstrichSans;
            src: url("fonts/ostrich-sans-bold.woff");
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 1200px;
            height: 600px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .site-title{
            text-align:center
        }
        .tile {
            margin-bottom: 10px;
            padding-top: 20px;
        }
        .tile:hover {
            cursor: pointer;
        }
        .tile img {
            transition: border 0.8s ease;
        }
        .tile img:hover {
            border: 10px solid #000;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .navbar {
            border: none;
        }
        .navbar-header {
            float: left;
            padding: 15px;
            text-align: center;
            width: 100%;
            padding-top: 25px;
            background-color: #000;
        }
        .navbar-brand{
            font-family: OstrichSans;
            float: none;
            font-size: 50px;
            line-height: 55px;
            color: #799;
        }
        .popular-header {
            font-family: OstrichSans;
            font-size: 80px;
        }
        .movie-container {
            position: relative;
        }
        .movies-header {
            position: absolute;
            top: 5%;
            width: 25%;
            line-height: 80px;
            padding: 0;
            left: -25%;
        }
        .show-container {
            position: relative;
        }
        .series-header {
            position: absolute;
            width: 25%;
            top: 0;
            left: -20%;
            line-height: 80px;
        }
        hr {
            margin-top: 35px;
            margin-bottom: 50px;
            border: 0;
            border-top: 10px dashed #000;
        }
        body {
            position: relative;
            background-color: #FFF11B;
        }
        .disclaimer {
            position: absolute;
            right: 5px;
            bottom: 5px;
        }
        .little-popcorn {
            width: 150px;
            position: absolute;
            top: 10px;
            left: 30px;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="navbar navbar-default" role="navigation">
      <div class="navbar-header">
        <img class="little-popcorn" src="imgs/little-popcorn.png">
        <a class="navbar-brand site-title" href="#">Fresh Tomatoes Trailers!</a>
      </div>
    </div>
    <div class="movie-container container">
        {movie_tiles}
        <div class="movies-header popular-header">Most Popular Movies: (Top 10) </div>
    </div>
    <hr>
    <div class="show-container container">
        {serie_tiles}
        <div class="series-header popular-header">Most Popular Shows: (Top 10) </div>
    </div>
    <span class="disclaimer"> Data fetched from <a href="https://www.themoviedb.org/" target="_blank"> The Movie DB </a></span>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 tile movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''
# A single show entry html template
show_tile_content= '''
<div class="col-md-6 col-lg-4 tile show-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{show_title}</h2>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        #Validating data consistency
        if(movie.trailer_youtube_url is not None):
            # Extract the youtube ID from the url
            youtube_id_match = re.search(
                r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
            youtube_id_match = youtube_id_match or re.search(
                r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
            trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                                  else None)
        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content

def create_show_tiles_content(series):
    # The HTML content for this section of the page
    content = ''
    for show in series:
        #Validating data consistency
        if(show.trailer_youtube_url is not None):
            # Extract the youtube ID from the url
            youtube_id_match = re.search(
                r'(?<=v=)[^&#]+', show.trailer_youtube_url)
            youtube_id_match = youtube_id_match or re.search(
                r'(?<=be/)[^&#]+', show.trailer_youtube_url)
            trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                                  else None)

        # Append the tile for the show with its content filled in
        content += show_tile_content.format(
            show_title=show.title,
            poster_image_url=show.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content


def open_movies_page(movies, series):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    movie_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies),
        serie_tiles=create_show_tiles_content(series)
    )

    # Output the file
    output_file.write(main_page_head + movie_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
