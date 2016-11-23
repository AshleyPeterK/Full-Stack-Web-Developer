import media  # Imports media.py file that has the Movie class definition

import fresh_tomatoes   # Imports fresh_tomatoes.py file that creates a webpage


# Creating six instances for the class Movie


jungle_book = media.Movie("Jungle Book",
                        "A fantastic adventure story set in the jungle"
                        "about an orphaned boy named Mowgli and animals",
                        "https://upload.wikimedia.org/wikipedia/en/a/a4/The_Jungle_Book_%282016%29.jpg",  # NOQA
                        "https://www.youtube.com/watch?v=5mkm22yO-bs")

saving_private_ryan = media.Movie("Saving Private Ryan",
                        "An absolute thriller where eight men will risk"
                        "their lives on a dangerous mission to find a"
                        "missing soldier",
                        "https://upload.wikimedia.org/wikipedia/en/a/ac/Saving_Private_Ryan_poster.jpg",  # NOQA
                        "https://www.youtube.com/watch?v=HyVuRpjmaAI")

bridge_of_spies = media.Movie("Bridge of Spies",
                        "A drama-packed movie showing the exchange"
                        "of two prisoners between the USSR and US"
                        "during the Cold war",
                        "https://upload.wikimedia.org/wikipedia/en/f/fa/Bridge_of_Spies_poster.jpg",  # NOQA
                        "https://www.youtube.com/watch?v=7JnC2LIJdR0")

zootopia = media.Movie("Zootopia",
                        "This is where a rabbit police officer and"
                        "a red fox con artist join hands to stop"
                        "a conspiracy",
                        "https://upload.wikimedia.org/wikipedia/en/e/ea/Zootopia.jpg",  # NOQA
                        "https://www.youtube.com/watch?v=jWM0ct-OLsM")

mercury_rising = media.Movie("Mercury Rising",
                        "See how an FBI agent will go to great lengths"
                        "to protect a nine year old boy whose life is"
                        "in constant danger",
                        "https://upload.wikimedia.org/wikipedia/en/a/a8/Mercuryrisingposter.jpg",  # NOQA
                        "https://www.youtube.com/watch?v=Lodj3ZT4tOU")

the_last_days_on_mars = media.Movie("The Last Days on Mars",
                        "A horror story that is set on planet Mars",
                        "https://upload.wikimedia.org/wikipedia/en/0/0e/Last_Days_on_Mars_Poster.jpg",  # NOQA
                        "https://www.youtube.com/watch?v=9_C8_xmixrg")

# The array that has the list of movies

movies = [zootopia, saving_private_ryan, the_last_days_on_mars,
          bridge_of_spies, jungle_book, mercury_rising]
# Creates a webpage having the movies list
fresh_tomatoes.open_movies_page(movies)
