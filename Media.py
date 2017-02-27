class Media():

    """

    Media class for creating media related objects. Since this is a trailer website, we will have different types of media with different trailers.
    I'd like to abstract the common properties of all media in this class

    """

    def __init__(self, title, storyline, trailer_youtube_url):
        self.title = title
        self.storyline = storyline
        self.trailer_youtube_url = trailer_youtube_url


class Show(Media):

    """
    Show class for defining TV show in our trailer website. Inherits from Media class
    Poster image and rating are particular to this class due to the possibility
    this information might come from a different source or processed in a different way

    """

    def __init__(self, title, story_line, trailer_youtube_url, poster_image_url, rating):
        Media.__init__(self, title, story_line, trailer_youtube_url)
        self.poster_image_url = poster_image_url
        self.rating = rating


class Movie(Media):

    """

    Movie class for creating movie objects. Inherits from Media class.
    Poster image and rating are particular to this class due to the possibility
    this information might come from a different source or processed in a different way

    """

    def __init__(self, title, story_line, trailer_youtube_url, poster_image_url, rating):
        Media.__init__(self, title, story_line, trailer_youtube_url)
        self.poster_image_url = poster_image_url
        self.rating = rating

