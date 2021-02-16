#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import os
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for , abort , flash
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from forms import *
# from forms import RegistrationForm, LoginForm
from datetime import datetime
from flask_migrate import Migrate
from models import *
from app import *

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#setting our home page route
@app.route('/')
def index():
  # venues = Venue.query.order_by(desc(Venue.created_date)).limit(10).all()
  # artists = Artist.query.order_by(desc(Artist.created_date)).limit(10).all()
  # return render_template('pages/home.html', venues=venues, artists=artists)
  #returing our home page
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  #declaring data array
  data = []
  # Query unique cities and states with distict
  unique_city = Venue.query.distinct(Venue.city, Venue.state).all()
  # Query all shows order by show start time 
  venues = db.session.query(Venue).all()
  #getting the city and state
  for city in unique_city:
    
    for venue in venues:
      if venue.city == city.city and venue.state == city.state:
        # declaring new venue object
        new_venue = {
          "city": city.city, 
          "state": city.state, 
          "venues":[{
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows":len(db.session.query(Show).filter(Show.venue_id == venue.id, Show.start_time >datetime.now()).all())}]}
      #append the venue to the data array to list it 
    data.append(new_venue)
  # when it finishes , return to venue page
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  
  # venue_search = Venue.query.whoosh_search(request.args.get('query')).all()
  #getting the search term from user input
  search_term = request.form.get('search_term', '')
  #filter the results by the search term used , using join
  # results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  results = db.session.query(Venue.id, Venue.name, func.count('*').label('num_upcoming_shows')).filter(Venue.name.like(
        f'%{search_term}%')).join(Show, Show.start_time > datetime.now(), isouter=True).group_by(Venue.id, Venue.name).all()
  #our results will be as countes results and showing the searched data
  response={
    "count": results.count(),#count the results
    "data": results# showing the results
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  #Query the venue and filter by the venue ud that was given
  venue = Venue.query.filter(Venue.id == venue_id).first_or_404()
  #declaring variable form date time 
  cur_date = datetime.now()
  #get the past shows by quering using join
  #past_shows = db.session.query(Show, Artist).filter(Show.venue_id == venue_id, Artist.id == Show.artist_id, Show.start_time < cur_date).all()
  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
      filter(
          Show.venue_id == venue_id,
          Show.artist_id == Artist.id,
          Show.start_time < datetime.now()
  ).all()
  #upcoming_shows = db.session.query(Show, Artist).filter(Show.venue_id == venue_id, Artist.id == Show.artist_id, Show.start_time > cur_date).all()
  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
        filter(
            Show.venue_id == venue_id,
            Show.artist_id == Artist.id,
            Show.start_time > datetime.now()
    ).all()
  #defining data
  data={
     "id": venue.id,
     "name": venue.name,
     "genres": [venue.genres],
     "address": venue.address,
     "city": venue.city,
     "state": venue.state,
     "phone": venue.phone,
     "website": venue.website,
     "facebook_link": venue.facebook_link,
     "seeking_talent": venue.seeking_talent,
     "seeking_description": venue.seeking_description,
     "image_link": venue.image_link,
     "past_shows": [{
        "artist_id":artist.id,
        "artist_name":artist.name,
        "artist_image_link":artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M"),
      } for show,artist in past_shows],
     "upcoming_shows": [{ 
        "artist_id":artist.id,
        "artist_name":artist.name,
        "artist_image_link":artist.image_link,
        "start_time":show.start_time.strftime("%m/%d/%Y, %H:%M"),
      } for show,artist in upcoming_shows],
     "past_shows_count": len(past_shows),
     "upcoming_shows_count": len(upcoming_shows),
   }

  # data = list(filter(lambda d: d['id'] == venue_id, data))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    #declaring our used form
    form = VenueForm(request.form)
    #declaring error object as False
    error = False
    #setting message variable 
    message = ''
    #check if the method coming from from is post
    if request.method == 'POST':
      #try these steps
      try:
        #declare a new object from Venue table
        data = Venue()
        #populating our data
        form.populate_obj(data)
        #then add the new venue to database
        db.session.add(data)
        #commit changes to save it
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
      #if there is error
      except:
        #incase errors appear set error = True and rollback the changes
        error = True
        #if error convert sys.exc_info() to string and print it
        message = str(sys.exc_info())
        #print error message in terminal
        print(str(sys.exc_info()))
        #flash the error message in the view page
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        db.session.rollback()#to undo the changes if error exists
      #finally we need to do this
      finally:
        #finally we need to close the session
        db.session.close()
    # return to home page when it finishes
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  #setting Error and message variable
  Error = False
  message = ''
  #try to delete the selected venue
  try:
    venue = request.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue was successfully deleted!')

  except:
    #incase errors appear set error = True and rollback the changes
    error = True
    #if error convert sys.exc_info() to string and print it
    message = str(sys.exc_info())
    #print error message in terminal
    print(str(sys.exc_info()))
    #flash the error message in the view page
    flash('An error occurred. Venue could not be deleted. ,  please try again')
    db.session.rollback()#to undo the changes if error exists
  finally:
    #finally we need to close the session
    db.session.close()
  return redirect(url_for('index'))


#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  # Query all artists 
  data = db.session.query(Artist).all()
  # when it finishes , return to artists page
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term', '')
  #results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  search_result = db.session.query(Artist.id, Artist.name, func.count('*').label('num_upcoming_shows')).filter(Artist.name.like(
        f'%{search_term}%')).join(Show, Show.start_time > datetime.now(), isouter=True).group_by(Artist.id, Artist.name).all()
  response={
    "count": results.count(),
    "data": results
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  #query the selecred artist
  artist = Artist.query.filter(Artist.id == artist_id).first_or_404()
  #declaring a variable from datetime
  cur_date = datetime.now()
  #getting the past shows using join
  #past_shows = db.session.query(Show, Venue).filter(Show.artist_id == artist_id, Venue.id == Show.venue_id, Show.start_time < cur_date).all()
  past_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
        filter(
            Show.artist_id == artist_id,
            Show.venue_id == Venue.id,
            Show.start_time < datetime.now()
    ).all()
  #getting the upcouming shows using join
  #upcoming_shows = db.session.query(Show, Venue).filter(Show.artist_id == artist_id, Venue.id == Show.venue_id, Show.start_time > cur_date).all()
  upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
        filter(
            Show.artist_id == artist_id,
            Show.venue_id == Venue.id,
            Show.start_time > datetime.now()
    ).all()
        #define our data
  data={
     "id": artist.id,
     "name": artist.name,
     "genres": [artist.genres],
     "city": artist.city,
     "state": artist.state,
     "phone": artist.phone,
     "website": artist.website,
     "facebook_link": artist.facebook_link,
     "seeking_venue": artist.seeking_venue,
     "seeking_description": artist.seeking_description,
     "image_link": artist.image_link,
     "past_shows": [{
        "venue_id":venue.id,
        "venue_name":venue.name,
        "venue_image_link":venue.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M"),
      } for show,venue in past_shows],
     "upcoming_shows": [{ 
        "venue_id":venue.id,
        "venue_name":venue.name,
        "venue_image_link":venue.image_link,
        "start_time":show.start_time.strftime("%m/%d/%Y, %H:%M"),
      } for show,venue in upcoming_shows],
     "past_shows_count": len(past_shows),
     "upcoming_shows_count": len(upcoming_shows),
   }
   #return show artist page
  return render_template('pages/show_artist.html', artist=data)

  
#  ----------------------------------------------------------------
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  #form used
  form = EditArtistForm()
  #query selected artist
  artist = Artist.query.get(artist_id)
  #define it
  artist={
    "id": artist.id ,
    "name": artist.name ,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": True if 'seeking_venue' in request.form else False,
    "seeking_description":artist.seeking_description,
    "image_link": artist.image_link
  }
 

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = EditArtistForm()
  Error = False
  message = ''
  try:
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.website = form.website.data
    artist.facebook_link = form.facebook_link.data
    artist.seeking_venue = form.seeking_venue
    artist.seeking_description =  form.seeking_description.data
    artist.image_link = form.image_link.data

    db.session.commit()
    flash('Artist ' + form.name.data + ' was successfully Updated!')
  except:
    Error = True
    db.session.rollback()
    message = str(sys.exc_info())
    print(str(sys.exc_info()))
    flash('Artist' + form.name.data + ' wasn\'t updated , there was an Error, try again please!')
  finally:
    #we need to end the session, finally
    db.session.close()

  # when finish , return to page
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  Error = False
  message = ''

  try:
    artist = request.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
    flash('Artist was successfully deleted!')

  except:
    #incase errors appear set error = True and rollback the changes
    error = True
    #if error convert sys.exc_info() to string and print it
    message = str(sys.exc_info())
    #print error message in terminal
    print(str(sys.exc_info()))
    #flash the error message in the view page
    flash('An error occurred. Artist could not be deleted. ,  please try again')
    db.session.rollback()#to undo the changes if error exists
  finally:
    #finally we need to close the session
    db.session.close()
  return redirect(url_for('index'))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  #query the selected venue
  venue = Venue.query.get(venue_id)

  #form used
  form = EditVenueForm(obj = venue)
  
  #when finish return to page
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = EditVenueForm(request.form)
  Error = False
  message = ''
  try:
    submited_venue = db.session.query(Venue).get(venue_id)
    submited_venue.name = form.name.data
    submited_venue.address = form.address.data
    submited_venue.city = form.city.data
    submited_venue.state = form.state.data
    submited_venue.phone = form.phone.data
    submited_venue.genres = request.form.getlist('genres')
    submited_venue.image_link = form.image_link.data
    submited_venue.facebook_link = form.facebook_link.data
    submited_venue.website = form.website.data
    submited_venue.seeking_talent = True if 'seeking_talent' in request.form else False
    submited_venue.seeking_description = form.seeking_description.data
    db.session.commit()
    flash('Venue ' + form.name.data + ' was successfully Updated!')
  except:
    Error = True
    db.session.rollback()
    message = str(sys.exc_info())
    print(str(sys.exc_info()))
    flash('Venue' + form.name.data + ' wasn\'t updated , there was an Error, try again please!')
  finally:
    #we need to end the session, finally
    db.session.close()
  # when finish , return to page
  return redirect(url_for('show_venue', venue_id=venue_id))


#  ----------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  form = ArtistForm(request.form)
  error = False
  message = ''

  if request.method == 'POST':

    try:
      #declare a new object from Artist table
      data = Artist()
      #populating our data
      form.populate_obj(data)
      #then add the new Artist to database
      db.session.add(data)
      #commit changes to save it
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      #incase errors appear set error = True and rollback the changes
      error = True
      #if error convert sys.exc_info() to string and print it
      message = str(sys.exc_info())
      #print error message in terminal
      print(str(sys.exc_info()))
      #flash the error message in the view page
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()#to undo the changes if error exists
    finally:
      #finally we need to close the session
      db.session.close()
  # return to home page when it finishes
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  #declaring data array
  #data = []
  # Query all shows order by show start time 
  #shows = Show.query.order_by(db.desc(Show.start_time))
  #listing shows
  #for show in shows:
    # declaring new show object
  #  new_show = {'show_id':show.id,'artist_id':show.artist_id,'venue_id':show.venue_id,'artist_name':show.artists.name,
  #  'venue_name':show.venues.name,'artist_image_link':show.artists.image_link,'start_time':str(show.start_time)}
    #append the show to the data array to list it 
  #  data.append(new_show)
  data = db.session.query(Show.venue_id,Venue.name.label('venue_name'),Show.artist_id,
        Artist.name.label("artist_name"),Artist.image_link.label("artist_image_link"), func.to_char(Show.start_time, "YYYY-MM-DD hh:mm:ss").label("start_time")).join(Artist).join(Venue).all()
  # when it finishes , return to shows page
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  error = False
  message = ''
  #check method
  if request.method == 'POST':
    #using try and expcept
    try:
      #declare a new object from Show table
      data = Show()
      #populating our data
      form.populate_obj(data)
      #then add the new Show to database
      db.session.add(data)
      #commit changes to save it
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    except:
      #incase errors appear set error = True and rollback the changes
      error = True
      #if error convert sys.exc_info() to string and print it
      message = str(sys.exc_info())
      #print error message in terminal
      print(str(sys.exc_info()))
      #flash the error message in the view page
      flash('An error occurred. Show could not be listed.')
      db.session.rollback()#to undo the changes if error exists
    finally:
      #finally we need to close the session
      db.session.close()
  # return to home page when it finishes
  return render_template('pages/home.html')


