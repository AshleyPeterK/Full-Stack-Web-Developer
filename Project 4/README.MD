#Project 4 - Design a Game API - Hangman API

##Project Overview

###Description
The goal of this project is to write an API for a game. This API  has several endpoints that enables anyone to build a Front-End / Web (UI) User Interface for the game.

###Aim
Learn to deploy a web app using the `Google App Engine` backed by Google Datastore so as to achieve unlimited scalability i.e the web app can function flawlessy even when its accessed by billions of users simultaneously.

###Tools and technologies used
- Python programming language version 2.7
- Sublime text editor
- Google App Engine
- Google API Explorer

##How to use the API

###API description
I have written an API for a guessing game called **Hangman**. This API has several endpoints e.g `get_user_scores` that can be tested with the Google API Explorer to check if they are all properly functioning.

###List of files in the Hangman game API folder
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper functions.

###Setting up the Hangman API
Replace the value of application in app.yaml file to the app ID you have registered in the Google App Engine admin console and would like to use to host your instance of this sample. 

- Visit https://console.developers.google.com/ to register and get an app ID.

  - Please ensure you have Python version 2.7, Google App engine launcher installed on your machine. Then start  the Google App engine launcher, add the Hangman game API folder and first run the application on local host by clicking 'Run'. Check the log for any errors by clicking the'Log' button. Next, deploy this app to Google App Engine by clicking 'Deploy'. Closely examine the log for any errors. Once the messages 'Process exited with code 0' and 'Completed update of app' get displayed, know that the app has been sucessfully deployed to Google App Engine.

  - To test the Hangman API endpoints, use the Google API Explorer tool by going to the below url in your   browser:

    https://**YOUR_APP_ID**.appspot.com/_ah/api/explorer
 
  - Click on the hangman API to see all the endpoints.

###Hangman Game Description
This is a one-player guessing game where you have to guess a randomly chosen word, by entering a single letter at a time. You have seven attempts to guess the word correctly else you lose the game. Each time you make a correct guess, the series of asterixes representing the word get filled with the correctly guessed letter. If you correctly guess all the letters in the word, all the asterixes dissapear and the word appears.
- Any game can be retrieved or played by using the path parameter **urlsafe_game_key**.
- You cannot guess an entire word nor can you input any numbers or special characters in a guess. 

###Score-Keeping in the Hangman game
- Any User can either win or lose a game.
- To know a User's Score, a simple mechanism has been implemented that computes the difference between the number of games won and the number of game lost for each user.
- Users' whose scores are zero get an email reminder every 12 hours telling them to improve their performance.

###List of API Endpoints 
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, min, max, attempts
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Min must be less than
    max. Also adds a task to a task queue to update the average moves remaining
    for active games.
     
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
    
 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new game state.
    - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.
    
 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).
    
 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms. 
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.
    
 - **get_average_attempts_remaining**
    - Path: 'games/average_attempts'
    - Method: GET
    - Parameters: None
    - Returns: StringMessage
    - Description: Gets the average number of attempts remaining for all games
    from a previously cached memcache key.

 - **get_user_games**
    - Path: 'games/user/{user_name}'
    - Method: GET
    - Parameters: None
    - Returns: GameForms
    - Description: Gets a user's active games
    
 - **cancel_game**
    - Path: 'game/{urlsafe_game_key}/cancel'
    - Method: PUT
    - Parameters: urlsafe_game_key
    - Returns: StringMessage
    - Description: Cancels any active game.

 - **get_high_scores**
    - Path: 'scores/highscores'
    - Method: GET
    - Parameters: number_of_results
    - Returns: RankingForms
    - Description: Provides the high scores 
    
 - **get_user_rankings**
    - Path: 'scores/rankings'
    - Method: GET
    - Parameters: None
    - Returns: RankingForms
    - Description: Provides ranking for all users
    
 - **get_game_history**
    - Path: 'sgame/{urlsafe_game_key}/history'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: StringMessage
    - Description: Reveals all User moves / guesses made in a specific game.  

###Forms description
 - **GameForm**
    - Represent's a Game's state. 
 - **HighScoreForm**
    - Handles the number of high scores
 - **NewGameForm**
    - Creates a new game.
 - **RankingForm**
    - Used for high scores and user ranking.
 - **ScoreForm**
    - Represents the score of a completed game.
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **StringMessage**
    - General purpose String container.
 - **MakeMoveForm**
    - Handles user moves.         
 - **RankingForms**
    - Enables multiple rankings.
 - **GameForms**
    - Returns multiple GameForms.   

###Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.

 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.

 - **Score**
    - Records completed games. Associated with Users model via KeyProperty. 

###ACKNOWLEGEMENT
Special thanks to `Udacity` for using their course materials to do this project. 








