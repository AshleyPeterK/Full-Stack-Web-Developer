#Project 2 - Tournament Results  

##Project Overview

###Description
Here, you need to write a **Python** module that uses a **PostgreSQL** database to keep track of players and matches in a game tournament. The game tournament will use the `Swiss system` for pairing up players in each round.   

###Aim
Learn to how create and use databases by utilizing **database schemas** and also learn how to manipulate the data inside these databases.

###Tools and technologies used
- Python programming language version 2.7
- PostgreSQL
- Vagrant Virtual Machine
 
##Package/ Folder contents
You will find the following files inside the package / folder of the Tournaments Results application:
- `tournament.sql`is where the database schema is created
- `tournament.py`provides access to  database created in tournament.sql 
- `tournament_test.py`checks if 'tournament.py' is working properly

##Running the Tournaments Results application
- Setup a `Vagrant Virtual Machine` using Git, Virtual Box and Vagrant software.
- First, fork the `fullstack-nanodegree-vm` repository so that you have a version of your own within your Github account.
- Clone your fullstack-nanodegree-vm repository to your computer with the below command syntax in your terminal program:

  `git clone PASTE_PATH_TO_REPOSITORY_HERE fullstack`

- Next, type **cd fullstack/vagrant**
- Power on the Virtual machine by typing **vagrant up**
- Login into the Virtual machine by typing **vagrant ssh**
- Navigate to the tournament folder by typing **cd /vagrant/tournament**
- Then type **psql** to log into PostgreSQL
- Next type **\i tournament.sql** to import the `tournament.sql` file
- Exit  PostgreSQL by typing **\q**
- Run the `tournament.py` file by typing **python tournament.py**
- Finally type **python tournament_test.py** to check if the Tournaments Results application is working properly.
  If the application is working properly, you will see a `Success! All tests pass!` result otherwise errors get displayed. 

##Copyright Information
You can use the source code here in any manner you wish without my permission. 


  








