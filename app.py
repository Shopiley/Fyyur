#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
from tokenize import group
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models  import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models: in ./models.py 
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
      date = dateutil.parser.parse(value)
  else:
      date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime



#----------------------------------------------------------------------------#
# Helper Functions.
#----------------------------------------------------------------------------#

def num_of_upcoming_shows(id):
  return Show.query.filter(Show.start_time > datetime.now(), Show.venue_id==id).count()


def num_of_past_shows(id):
  return Show.query.filter(Show.start_time < datetime.now(), Show.venue_id==id).count()


def createSearchResponseBody(search_count, search_result):
  response={
    "count": search_count,
    "data": [] 
  }

  for result in search_result:
    venue={
      "id":result.id,
      "name": result.name,
      "num_upcoming_shows": num_of_upcoming_shows(result.id)
    }

    response["data"].append(venue)
  return response



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  VenuesList=[]

  cities_states = Venue.query.with_entities(Venue.city, Venue.state).distinct().order_by(Venue.city).order_by(Venue.state).all()

  combinedList = [] 
  for city, state in cities_states:
    groupedVenues = Venue.query.filter(Venue.city == city, Venue.state == state).all()
    groupedVenuesLocation = [city, state, groupedVenues]
    combinedList.append(groupedVenuesLocation)

  def createResponseObject(responseList):
    for x in responseList:
      object= {
        "city": x[0],
        "state": x[1],
        "venues": []
      }
      
      venues = x[2]
      for y in venues:
        sub_object={
          "id": y.id,
          "name": y.name,
          "num_upcoming_shows": num_of_upcoming_shows(y.id)
        }

        object["venues"].append(sub_object)

      VenuesList.append(object)

  createResponseObject(combinedList)

  return render_template('pages/venues.html', areas=VenuesList)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  #case sensitive search on artists with partial string search. 
  search_term = request.form.get('search_term', '')
  search_result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  search_count = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).count()
  response = createSearchResponseBody(search_count, search_result)  #reference to a function defined above in the helper function section 

  return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  requestedVenue = Venue.query.get(venue_id)
  print(requestedVenue)

  def past_shows(venue_id):
    return db.session.query(Show.venue_id, Show.artist_id, Artist.name, Artist.image_link, Show.start_time).join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()

  def upcoming_shows(venue_id):
    return db.session.query(Show.venue_id, Show.artist_id, Artist.name, Artist.image_link, Show.start_time).join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()

  venueData={
    "id": requestedVenue.id,
    "name": requestedVenue.name,
    "genres": requestedVenue.genres,
    "address": requestedVenue.address,
    "city": requestedVenue.city,
    "state": requestedVenue.state,
    "phone": requestedVenue.phone,
    "website": requestedVenue.website_link,
    "facebook_link": requestedVenue.facebook_link ,
    "seeking_talent": requestedVenue.seeking_talent,
    "seeking_description": requestedVenue.seeking_description,
    "image_link": requestedVenue.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": num_of_past_shows(venue_id), #use len()
    "upcoming_shows_count": num_of_upcoming_shows(venue_id),
  }

  past_shows = past_shows(venue_id)
  for show in past_shows:
    past={
      "artist_id": show.artist_id,
      "artist_name": show.name,
      "artist_image_link": show.image_link,
      "start_time": show.start_time
    }

    venueData["past_shows"].append(past)

  upcoming_shows = upcoming_shows(venue_id)
  for show in upcoming_shows:
    upcoming={
      "artist_id": show.artist_id,
      "artist_name": show.name,
      "artist_image_link": show.image_link,
      "start_time": show.start_time
    }

    venueData["past_shows"].append(upcoming)

  return render_template('pages/show_venue.html', venue=venueData)



#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    form = VenueForm(request.form)
    venue = Venue(
      name=form.name.data,
      city=form.city.data, 
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      facebook_link=form.facebook_link.data,
      image_link=form.image_link.data,
      website_link=form.website_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data
    )
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

  finally: 
    db.session.close()
  
  return render_template('pages/home.html')


@app.route('/venues/<venue_id>/delete', methods=['GET', 'DELETE'])
def delete_venue(venue_id):
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage...DONE

  DeleteVenue = Venue.query.get(venue_id)
  try:
    db.session.delete(DeleteVenue)
    db.session.commit()
    flash("Venue: " + DeleteVenue.name + " was successfully deleted.")
  
  except:
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
  
  return redirect(url_for('index'))



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  ArtistsList = db.session.query(Artist.id, Artist.name).all()

  return render_template('pages/artists.html', artists=ArtistsList)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  #case sensitive search on artists with partial string search. 
  search_term = request.form.get('search_term', '')
  search_result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  search_count = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).count()
  response = createSearchResponseBody(search_count, search_result) #reference to a function defined above in the helper function section 

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # replace with real artist data from the artist table, using artist_id
  requestedArtist = Artist.query.get(artist_id)

  def past_shows(artist_id):
    return db.session.query(Show.venue_id, Show.artist_id, Venue.name, Venue.image_link, Show.start_time).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()

  def upcoming_shows(artist_id):
    return db.session.query(Show.venue_id, Show.artist_id, Venue.name, Venue.image_link, Show.start_time).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()

  ArtistData={
    "id": requestedArtist.id,
    "name": requestedArtist.name,
    "genres": requestedArtist.genres,
    "city": requestedArtist.city,
    "state": requestedArtist.state,
    "phone": requestedArtist.phone,
    "website": requestedArtist.website_link,
    "facebook_link": requestedArtist.facebook_link ,
    "seeking_venue": requestedArtist.seeking_venue,
    "seeking_description": requestedArtist.seeking_description,
    "image_link": requestedArtist.image_link,
    "past_shows": [], 
    "upcoming_shows": [],
    "past_shows_count": num_of_past_shows(artist_id), #use len()
    "upcoming_shows_count": num_of_upcoming_shows(artist_id),

  }
  past_shows = past_shows(artist_id)
  for show in past_shows:
    past={
      "venue_id": show.venue_id,
      "venue_name": show.name,
      "venue_image_link": show.image_link,
      "start_time": show.start_time
    }

    ArtistData["past_shows"].append(past)

  upcoming_shows = upcoming_shows(artist_id)
  for show in upcoming_shows:
    upcoming={
      "venue_id": show.venue_id,
      "venue_name": show.name,
      "venue_image_link": show.image_link,
      "start_time": show.start_time
    }

    ArtistData["past_shows"].append(upcoming)

  return render_template('pages/show_artist.html', artist=ArtistData)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

   #  populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  try:
    artist_to_be_edited = Artist.query.get(artist_id)   

    artist_to_be_edited.name = form.name.data
    artist_to_be_edited.city = form.city.data 
    artist_to_be_edited.state = form.state.data
    artist_to_be_edited.phone = form.phone.data
    artist_to_be_edited.genres = form.genres.data
    artist_to_be_edited.facebook_link = form.facebook_link.data
    artist_to_be_edited.image_link = form.image_link.data
    artist_to_be_edited.website_link = form.website_link.data
    artist_to_be_edited.seeking_venue = form.seeking_venue.data
    artist_to_be_edited.seeking_description = form.seeking_description.data
    db.session.add(artist_to_be_edited)
    db.session.commit()

    flash('Artist ' + form.name.data + ' was successfully updated!')
  
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + form.name.data + ' could not be updated.')

  finally: 
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  #populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  try:
    venue_to_be_edited = Venue.query.get(venue_id)   

    venue_to_be_edited.name = form.name.data
    venue_to_be_edited.city = form.city.data 
    venue_to_be_edited.state = form.state.data
    venue_to_be_edited.address = form.address.data
    venue_to_be_edited.phone = form.phone.data
    venue_to_be_edited.genres = form.genres.data
    venue_to_be_edited.facebook_link = form.facebook_link.data
    venue_to_be_edited.image_link = form.image_link.data
    venue_to_be_edited.website_link = form.website_link.data
    venue_to_be_edited.seeking_talent = form.seeking_talent.data
    venue_to_be_edited.seeking_description = form.seeking_description.data
    db.session.add(venue_to_be_edited)
    db.session.commit()

    flash('Venue ' + form.name.data + ' was successfully updated!')
  
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + form.name.data + ' could not be updated.')

  finally: 
    db.session.close()


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  try:
    form = ArtistForm(request.form)
    artist = Artist(
      name=form.name.data,
      city=form.city.data, 
      state=form.state.data,
      phone=form.phone.data,
      genres=form.genres.data,
      facebook_link=form.facebook_link.data,
      image_link=form.image_link.data,
      website_link=form.website_link.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data
  )
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + form.name.data + ' was successfully listed!')
  
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
  
  finally: 
    db.session.close()  
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  shows = db.session.query(Show.venue_id, Venue.name, Show.artist_id, Artist.name, Artist.image_link, Show.start_time).join(Venue).join(Artist).filter(Show.venue_id == Venue.id, Show.artist_id == Artist.id).all()
  print(shows)
  ShowsList=[]
  for show in shows:
    object={
      "venue_id": show[0],
      "venue_name": show[1],
      "artist_id": show[2],
      "artist_name": show[3],
      "artist_image_link": show[4],
      "start_time": show[5]
    }
    ShowsList.append(object)
  return render_template('pages/shows.html', shows=ShowsList)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  try:
    form = ShowForm(request.form)
    # insert form data as a new Show record in the db, instead
    show = Show(
      artist_id=form.artist_id.data,
      venue_id=form.venue_id.data,
      start_time=form.start_time.data
      )  
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  # on unsuccessful db insert, flash an error instead.
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')

  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
