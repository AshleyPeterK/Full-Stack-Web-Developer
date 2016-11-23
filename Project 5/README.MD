#Project 5 - Linux Server Configuration

##Project Overview

###Description
The principal objective of this project is to deploy a web app that was developed for **Project 3 (Item Catalog)** of the Udacity Fullstack Web Developer Nanodegree program. This web app needs to be hosted on a virtual server in `Amazon’s Elastic Compute Cloud (EC2)`. 

###Aim
Configure a new Linux server to host a web application. This will involve performing the following major tasks:
- Installing software updates.
- Setting up a Web-server e.g Apache.
- Setting up a Database-server.
- Ensuring the best possible security. 

###Tools and technologies used
- Git
- Amazon’s Elastic Compute Cloud (EC2) 

##How to acesss the server
- IP address is **35.162.229.47**
- SSH port is **2200**
- Complete URL for the hosted web application is **ec2-35-162-229-47.us-west-2.compute.amazonaws.com**

*Please note: after my Graduation from the Udacity Full Stack Web Developer program, the URL **ec2-35-162-229-47.us-west-2.compute.amazonaws.com** is no longer active.* 

##Summary of software installed
- Installed Finger to check if new user created 

  `sudo apt-get install finger`
- Installed  Apache as the Web-server 

  `sudo apt-get install apache2`

- Installed mod_wsgi which is an Apache HTTP Server module

  `sudo apt-get install libapache2-mod-wsgi`    

- Installed  PostgreSQL as the Database-server

  `sudo apt-get install postgresql postgresql-contrib`

- Installed Git

  `sudo apt-get install git`

##Summary of configuration changes made
- Created a new user named **grader**

  `adduser grader`

- Check if the new user 'grader' is there

  `finger grader`  

- Gave the user 'grader' the permission to **sudo**

  `touch /etc/sudoers.d/grader` followed by

  `nano /etc/sudoers.d/grader` placed the text **grader ALL=(ALL:ALL)ALL**

- Updated all currently installed packages

  `sudo apt-get update` followed by

  `sudo apt-get upgrade`

- Changed the SSH port from 22 to 2200

  `nano /etc/ssh/sshd_config` , followed by `sudo service ssh restart`

- Configured the **Uncomplicated Firewall (UFW)** to only allow incoming connections for SSH 
  (port 2200), HTTP (port 80), and NTP (port 123)

  `sudo ufw default deny incoming`

  `sudo ufw allow 2200/tcp`

  `sudo ufw allow 80/tcp`

  `sudo ufw allow 123/udp`

  `sudo ufw enable`

- Enforced Key-based authentication

  `ssh-keygen`

  `ssh-copy-id grader@35.162.229.47 -p 2200`

  - Created a Pass Phrase which is **anderson1#**

  - Disabled both **Root Login** and **Password Authentication**
      
     `sudo nano /etc/ssh/sshd_config` and set 'PasswordAuthentication' to **no** and 'PermitRootLogin' to **no**
  - Restart the service with `sudo service ssh restart`  

- Configured the local timezone to **UTC**

  `sudo dpkg-reconfigure tzdata` select 'None of the above' and then 'UTC'

- Configured the PostgreSQL database-server to properly serve data for **Python Flask Web 
Application ( Restaurant Menu Application)**

  `sudo nano /etc/postgresql/9.3/main/pg_hba.conf` ensures that remote connections are not allowed.

  - created user **catalog** with limited permissions

  `sudo su - postgres`

  `psql`
  
  `CREATE USER catalog WITH PASSWORD '[THE_USERS_PASSWORD]' CREATEDB;`
  
  `\du`
  
  `CREATE DATABASE restaurantmenuwithusers WITH OWNER catalog;`

  `\c restaurantmenuwithusers` 

  `REVOKE ALL ON SCHEMA public FROM public;` 

  `GRANT ALL ON SCHEMA public TO catalog;`

  `\q`

  `exit` 

- Setup Git as follows:

  `git config --global user.name "Ashley peter"`

  `git config --global user.email "ashpk@ymail.com"`

- Configured Apache web-server to serve  the Python Flask Web Application ( Restaurant Menu Application)

  `cd /var/www`

  `sudo mkdir restaurantmenuapp`

  `cd restaurantmenuapp` then clone the **Restaurant Menu Application** from the **AshleyPeterK/restaurantmenuapp** github repository.

  `sudo git clone https://github.com/AshleyPeterK/restaurantmenuapp.git`

  - Make .git directory inaccessible by `sudo nano .htaccess` and add the line **RedirectMatch 404 /\.git**

  - change 'application.py' to `__init__.py` with `sudo mv application.py __init__.pyc

  - Replace this line of code `engine = create_engine('sqlite:///restaurantmenuwithusers.db')` in `__init__.py`,`database_setup.py` and `lotsofmenus.py` with this line of code `engine = create_engine('postgresql://catalog:postman@localhost/restaurantmenuwithusers')`

  - Makesure **mod_wsgi** is enabled using `sudo a2enmod wsgi`

  - Created a **virtual environment** for the flask application to run. I aslo installed the necessary Python   packages for the Flask app to run e.g sqlalchemy.
  
  ```
    sudo apt-get install python-pip

    sudo apt-get install libpq-dev python-dev

    sudo pip install virtualenv

    sudo virtualenv venv

    sudo chmod -R 777 venv

    source venv/bin/activate

    pip install Flask

    pip install requests

    pip install sqlalchemy

    pip install http://pypi.python.org/packages/source/p/psycopg2/psycopg2-2.4.tar.gz#md5=24f4368e2cfdc1a2b03282ddda814160

    install --upgrade oauth2client

    install httplib2

    deactivate
    ```
  - Create the database for the Flask app by running:

    `python database_setup.py`
  - Load the database with items

    `python lotsofmenus.py`

  - testrun the flask app using
  
    `python __init__.py`

  - Setup a new virtual host

    `sudo nano /etc/apache2/sites-available/restaurantmenuapp.conf`

    ```   
    <VirtualHost *:80>
      ServerName 35.162.229.47
      ServerAdmin admin@35.162.229.47
      ServerAlias ec2-35-162-229-47.us-west-2.compute.amazonaws.com
      WSGIScriptAlias / /var/www/restaurantmenuapp/restaurantmenuapp.wsgi
      WSGIDaemonProcess restaurantmenuapp python-path=/var/www/restaurantmenuapp:/var/www/restaurantmenuapp/ve$
      WSGIProcessGroup restaurantmenuapp
      <Directory /var/www/restaurantmenuapp/restaurantmenuapp/>
          Order allow,deny
          Allow from all
      </Directory>
      Alias /static /var/www/restaurantmenuapp/restaurantmenuapp/static
      <Directory /var/www/restaurantmenuapp/restaurantmenuapp/static/>
          Order allow,deny
          Allow from all
      </Directory>
      ErrorLog ${APACHE_LOG_DIR}/error.log
      LogLevel warn
      CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    ```
  - Enable the virtual host with `sudo a2ensite restaurantmenuapp`   

  - Create a .wsgi file to serve the Flask application

    `cd /var/www/restaurantmenuapp`

    `sudo nano restaurantmenuapp.wsgi` and enter the following

    ```
    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/restaurantmenuapp/")

    from restaurantmenuapp import app as application
    application.secret_key = 'Add your secret key'
    ``` 

  - Restart Apache with `sudo service apache2 restart`

## Handling 3rd Party authentication for the Flask app (Restaurant Menu Application) 
- For the Google Sign-in
  - Head to [Google Developers Console](https://console.developers.google.com) and add http://ec2-35-162-229-47.us-west-2.compute.amazonaws.com to **Authorized JavaScript** origins and **Authorized redirect URIs**

- For Facebook Sign-in
  - Go to [Facebook Developers Console](https://developers.facebook.com) and add http://ec2-35-162-229-47.us-west-2.compute.amazonaws.com to **OAuth Redirect URI**.

##List of third-party resources used for this project
- [DigitalOcean: Flask on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- [AskUbuntu: Update/Upgrade Packages:](http://askubuntu.com/questions/94102/what-is-the-difference-between-apt-get-update-and-upgrade)
- [Postgresql: Create Role](http://www.postgresql.org/docs/8.2/static/sql-createrole.html)  
- [DigitalOcean: Initial Server Setup with Ubuntu](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-14-04)
- [PlusBryan: 5 Minutes on a Server](http://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers) 
- [DigitalOcean: Postgresql on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)  








  

  

















      














  



















