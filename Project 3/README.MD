#Project 3 - Item Catalog  

##Project Overview

###Description
Develop a Web Application that will provide a list of items within a variety of categories. Implement a User registration and Authentication mechanism so that only registered users will have the ability to post, edit and delete their own items.   

###Aim
Learn to build a powerful **Modern Data-driven Web Application** using `Python` and related technologies like `Sql Alchemy`.

###Tools and technologies used
- Python programming language version 2.7
- SQLite
- Flask framework
- Sql Alchemy 
- Vagrant Virtual Machine

##Specific description
I have developed a **Restaurant Menu Web Application** that conforms to the set of guidelines for the Project. The purpose of the  Restaurant Menu Web Application is to allow users to view restaurants and their respective menu items. Logged-in users will have the ability to view, add, edit, and delete both menu items and restaurants which that he/ she created but NOT of other users.

##Package/ Folder contents
Ensure you have the 'catalog' folder with you with all the following files and folders inside:
- lotsofmenus.py
- database_setup.py
- application.py
- static folder
- templates folder
- fb_client_secrets.json
- client_secrets.json

##How to run the Restaurant Menu Web Application
- Setup a Vagrant Virtual Machine using Git, Virtual Box and Vagrant software. Also ensure that Python version 2.7 is installed in your computer.
- First, fork the `fullstack-nanodegree-vm` repository so that you have a version of your own within your Github account.
- Clone your fullstack-nanodegree-vm repository to your computer with the below command syntax in the Git bash terminal ( remember to run the Git bash program as an administrator):
 - `git clone PASTE_PATH_TO_REPOSITORY_HERE fullstack`
- First type **cd fullstack/vagrant**, press enter
- Type **vagrant up** and press enter so as to power on the Vagrant Virtual Machine
- Type **vagrant ssh** and press enter to log into the  Vagrant Virtual Machine
- Next type **cd /vagrant**  and  press enter
- Type **cd catalog**, press enter
- Now to sucessfully access the 'Restaurant Menu Web app' on a web browser, execute the following below steps in sequence :
 - **Step 1:** type `python database_setup.py`and press enter to initialize the database of the Restaurant Menu Web app.
 - **Step 3:** type `python lotsofmenus.py` and press enter to populate the Restaurant Menu Web app's database with restaurants and menu items.
 - **Step 3:** type  `python application.py`  and press enter to start the Flask application (application.py), then to view the  Restaurant Menu Web app, go to **http://localhost:8000** on your web browser.

 ##User privileges on the Restaurant Menu Web App
 - For a Logged-in user: able to view, add, edit, and delete both menu items and restaurants which he or she created but NOT of other users.
 - For a Visitor (a person who has not Logged-in ) : only be able to view both menu items and restaurants but CANNOT add, edit, or delete anything.

 ##Viewing Restaurant Information with JSON
  - Go to following URLs:
    - `http://localhost:8000/restaurant/JSON` will show all restuarants.
    - `http://localhost:8000/<int:restaurant_id>/menu/JSON`  will show a specific restaurant and all its menu items. Like *http://localhost:8000/restaurant/1/menu/JSON*
    - `http://localhost:8000/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON` will show a specific restaurant and a specific menu item of that particular restaurant. Like *http://localhost:8000/restaurant/1/menu/2/JSON*

 ##ACKNOWLEGEMENT
 Special thanks to `Udacity` for using their materials from the course ud330 to do this project.   




 



  








