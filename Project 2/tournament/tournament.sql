-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Check if database already exists and drop if it does
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Connects to the tournament database
\c tournament

-- Creating the PLAYERS table which will have Player IDs and Names
CREATE TABLE PLAYERS (
  id SERIAL PRIMARY KEY,
  name varchar(255)
);

-- Creating MATCHES table which will store all Tournament Matches
CREATE TABLE MATCHES (
  match_id SERIAL PRIMARY KEY,
  winner int references PLAYERS(id),
  loser int references PLAYERS(id)
);

-- View that lists Player IDs and number of wins
CREATE VIEW player_wins AS
  SELECT PLAYERS.id, COUNT(MATCHES.winner) AS wins
  FROM PLAYERS
  LEFT JOIN MATCHES
  ON PLAYERS.id = MATCHES.winner
  GROUP BY PLAYERS.id
  ORDER BY wins DESC;



-- View that lists number of Matches and Player IDs
CREATE VIEW count_matches AS
  SELECT PLAYERS.id, COUNT(MATCHES.match_id) AS match
  FROM PLAYERS
  LEFT JOIN MATCHES
  ON PLAYERS.id = winner or PLAYERS.id = loser
  GROUP BY PLAYERS.id
  ORDER BY match DESC;



-- View that serves as a Scoreboard which lists number of wins and Matches for all Players
CREATE VIEW scoreboard AS
  SELECT PLAYERS.id, PLAYERS.name, player_wins.wins as wins,
  count_matches.match as match
  FROM PLAYERS, player_wins, count_matches
  WHERE PLAYERS.id = player_wins.id and player_wins.id = count_matches.id;