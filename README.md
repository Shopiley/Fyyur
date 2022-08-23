Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

I built the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

## Overview

Along with the views and controllers are defined in this application, I implemented models and model interactions to be able to store retrieve, and update data from a database. The site is capable of doing the following using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.


## Tech Stack (Dependencies)

The tech stack I used includes the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** ORM library of choice
 * **PostgreSQL** database of choice
 * **Python3** and **Flask** server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
 * **HTML**, **CSS**, and **Javascript** with Bootstrap 3 for the website's frontend.

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` --Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` --  Defines the forms used to create new artists, shows, and venues.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data, connects and manipulates the database and renders views with data to the user, based on the URL.
* Models in `Models.py` --  Defines the data models that set up the database tables.
* `config.py` -- Stores configuration variables and instructions, separate from the main application code. 


## Development Setup
First, install Flask if you haven't already.
```
$ cd ~
$ sudo pip3 install Flask
```
To start and run the local development server,

1. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

2. **Install the dependencies:**
```
pip install -r requirements.txt
```

3. **Run the development server:**
```
set FLASK_APP=myapp
set FLASK_DEBUG=true # enables debug mode
python3 app.py
```

4. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

