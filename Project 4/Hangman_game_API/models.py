"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb
import urllib2


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()


class Game(ndb.Model):
    """Game object"""
    target = ndb.StringProperty(required=True)
    attempts_allowed = ndb.IntegerProperty(required=True)
    attempts_remaining = ndb.IntegerProperty(required=True, default=7)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    users_word = ndb.StringProperty(required=True)
    history = ndb.StringProperty(repeated=True)

    @classmethod
    def new_game(cls, user, attempts):
        """Creates and returns a new game"""
        # Random word generator inspired from this stack overflow post:
        # http://stackoverflow.com/questions/18834636/random-word-generator-python
        word_site = 'http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain'
        response = urllib2.urlopen(word_site)
        txt = response.read()
        words = txt.splitlines()

        chosen_target = random.choice(words)

        game = Game(user=user,
                    target=chosen_target,
                    attempts_allowed=attempts,
                    attempts_remaining=attempts,
                    game_over=False,
                    users_word = word_of_asterixes(chosen_target),
                    history = [])
        game.put()
        return game

    def update_users_word(self, letter):
        """Update the user's word, usually when a move's been made"""
        word_as_list = list(self.users_word)

        # Find where guessed letter occurs in target word and add it on
        # those positions in user's word
        for pos in self.find_letter_positions_in_word(letter, self.target):
            word_as_list[pos] = letter

        self.users_word = ''.join(word_as_list)


    def find_letter_positions_in_word(self, letter, word):
        """Helper method that find letter occurencies in a given word"""
        pos_list = []

        for i in range (0, len(word)):
            if word[i] == letter:
                pos_list.append(i)

        return pos_list


    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.users_word = self.users_word
        form.message = message
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    guesses = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), guesses=self.guesses)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)
    users_word = messages.StringField(6, required=True)

class GameForms(messages.Message):
    """Return multiple GameForms"""
    games = messages.MessageField(GameForm, 1, repeated=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    attempts = messages.IntegerField(4, default=7)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    guess = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)

class RankingForm(messages.Message):
    """Ranking form for high scores and user ranking"""
    user_name = messages.StringField(1, required=True)
    score = messages.IntegerField(2, required=True)

class RankingForms(messages.Message):
    """Multiple rankings"""
    rankings = messages.MessageField(RankingForm, 1, repeated=True)

class HighScoreForm(messages.Message):
    """Used to limit the number of high scores"""
    number_of_results = messages.IntegerField(1, default=5)


def word_of_asterixes(word):
    """Compute a word made up of asterixes (helper)"""
    wd = ''
    for i in range (0, len(word)):
        wd += '*'
    return wd
