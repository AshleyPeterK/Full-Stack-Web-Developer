import webbrowser  # Importing the webbrowser module
# Definition of the class Movie


class Movie():
                def __init__(self, movie_title, movie_storyline, poster_image,
                             trailer_youtube):  # Defining the constructor
                            # Initialization of instance variables
                            self.title = movie_title
                            self.storyline = movie_storyline
                            self.poster_image_url = poster_image
                            self.trailer_youtube_url = trailer_youtube
