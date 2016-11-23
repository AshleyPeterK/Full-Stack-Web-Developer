# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""

# --------- Imports ----------

import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game, Score
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm,\
    ScoreForms, RankingForm, RankingForms, HighScoreForm, GameForms
from utils import get_by_urlsafe

from utils import get_wins_minus_losses

# --------- Request Templates ----------

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))

HIGH_SCORES_REQUEST = endpoints.ResourceContainer(HighScoreForm)

MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'

# --------- Game API ----------

@endpoints.api(name='hangman', version='v1')
class HangmanAPI(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')

        game = Game.new_game(user.key, request.attempts)

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('You can now start playing Hangman!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""

        # Raise an error if user's guess isn't a letter
        if (self.not_valid(request.guess)):
            raise endpoints.BadRequestException('Guess is not a letter')

        # If game is already over, prompt user!
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over! The word was ' + game.target)

        # Update word from user's guess
        game.update_users_word(request.guess)

        # Check if user has won after this guess
        if game.users_word == game.target:
            game.end_game(True)
            return game.to_form('You win!')

        # Check if his guess was valid or not
        if request.guess in game.target:
            msg = 'Guessed letter is part of word'
            valid_or_not = 'valid'
        else:
            msg = 'Guessed letter is not part of word'
            valid_or_not = 'invalid'
            game.attempts_remaining -= 1

        # Append the move to the game's history
        game.history.append('(' + request.guess + ', ' + valid_or_not + ' guess)')

        # If user has no more attempts, he lost!
        if game.attempts_remaining < 1:
            game.end_game(False)
            return game.to_form(msg + '. Game over! The word was ' + game.target)
        # If not, continue playing
        else:
            game.put()
            return game.to_form(msg + '. The word looks like this: ' \
                                    + game.users_word)

    # Checks validity of a guess
    def not_valid(self, guess):
        return len(guess) != 1 or guess < 'a' or guess > 'z'

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()

        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')

        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(response_message=StringMessage,
                      path='games/average_attempts',
                      name='get_average_attempts_remaining',
                      http_method='GET')
    def get_average_attempts(self, request):
        """Get the cached average moves remaining"""
        return StringMessage(message=memcache.get(MEMCACHE_MOVES_REMAINING) or '')


    @endpoints.method(response_message=RankingForms,
                      path='scores/rankings',
                      name='get_user_rankings',
                      http_method='GET')
    def get_rankings(self, request):
        """Get all user rankings"""

        return RankingForms(rankings = self.determine_rankings())


    def determine_rankings(self):
        """Create a list of all the user rankings"""
        users = User.query()
        items = []

        # get and add each user's ranking
        for user in users:
            items.append(RankingForm(user_name = user.name,
                                     score = get_wins_minus_losses(user)))

        return items


    @endpoints.method(response_message=RankingForms,
                      request_message=HIGH_SCORES_REQUEST,
                      path='scores/highscores',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Get high scores"""

        # Sor rankings and return the first number_of_results rankings2
        results = self.sort_rankings(self.determine_rankings()) \
                  [0:request.number_of_results]

        return RankingForms(rankings = results)


    def sort_rankings(self, items):
        """Sort rankings by score, using a naive, bubble-sort strategy"""
        for i in range (0, len(items)):
            for j in range (1, len(items)):
                if items[i].score < items[j].score:
                    temp = items[i]
                    items[i] = items[j]
                    items[j] = temp

        return items


    @endpoints.method(request_message = USER_REQUEST,
                      response_message = GameForms,
                      path='games/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Get an user's active games"""
        user = User.query(User.name == request.user_name).get()

        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')

        # Get only games that are active and belong to this user
        games = Game.query(Game.user == user.key)
        games = games.filter(Game.game_over == False)

        return GameForms(games=[game.to_form("Good luck!") for game in games])


    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game/{urlsafe_game_key}/cancel',
                      name='cancel_game',
                      http_method='PUT')
    def cancel_game(self, request):
        """Cancel an active game."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)

        if game:
            if game.game_over == False:
                # Cancel game
                game.game_over = True
                game.attempts_remaining = 0
                game.put()
                return StringMessage(message='Game successfully cancelled!')
            else:
                raise endpoints.BadRequestException('Game is already over.')
        else:
            raise endpoints.NotFoundException('Game not found!')


    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game/{urlsafe_game_key}/history',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Get a game's history (moves made so far)"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)

        if game:
            return StringMessage(message='History: ' + str(game.history))
        else:
            raise endpoints.NotFoundException('Game not found!')



    @staticmethod
    def _cache_average_attempts():
        """Populates memcache with the average moves remaining of Games"""
        games = Game.query(Game.game_over == False).fetch()
        if games:
            count = len(games)
            total_attempts_remaining = sum([game.attempts_remaining
                                        for game in games])
            average = float(total_attempts_remaining)/count
            memcache.set(MEMCACHE_MOVES_REMAINING,
                         'The average moves remaining is {:.2f}'.format(average))


api = endpoints.api_server([HangmanAPI])
