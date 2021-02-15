#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from app import db
from sqlalchemy.orm import relationship


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# Define the Venue model
class Venue(db.Model):
    #__tablename__ = 'Venue'#setting table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique = True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable = False, default='/static/img/venue-pic.jpg')
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String(120)), nullable = False)
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    #many to many relationship with Artist model
    shows = db.relationship('Show', backref='venues', lazy = True, cascade = "save-update, merge, delete")

    #  __repr__ should return a printable representation of the object
    def __repr__(self):
      return f'<Venue {self.id} name: {self.name}>'

#---------------------------------------------------------------------------#

#define the Artist model
class Artist(db.Model):
   # __tablename__ = 'Artist'#setting table name
    #setting table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False, default='/static/img/default-facebook-profile-pic.jpg')
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #missing columns
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
    #setting many to mant relationship with venue table
    shows = db.relationship('Show', backref='artists', lazy = True, cascade = 'save-update, merge, delete')

    #__repr__ should return a printable representation of the object
    def __repr__(self):
      return f'<Artist {self.id} name: {self.name}>'

#---------------------------------------------------------------------------#

#setting the association table between venue and artist
class Show(db.Model):
  #__tablename__ = 'shows'#setting table name
  #setting table columns
  id = db.Column(db.Integer, primary_key = True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  #venue = db.relationship(Venue)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable = False)
  #artist = db.relationship(Artist)
  #upcoming = db.Column(db.Boolean, nullable = False , default = True)
  start_time = db.Column(db.DateTime, nullable = False)
  #venue_name = db.Column(db.String(50))
  #artist_name = db.Column(db.String(50))

  #__repr__ should return a printable representation of the object
  def __repr__(self):
    return f'<Show {self.id}, Artist {self.artist_id}, Venue {self.venue_id}>'


#---------------------------------------------------------------------------#



db.create_all()
db.session.commit()
