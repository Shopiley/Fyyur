from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
        return f'<Venue {self.id} {self.venue_id} {self.artist_id} {self.start_time}>'


 
class Venue(db.Model): 
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False) 
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)   
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(120), nullable=True)
    artists = db.relationship('Artist', secondary='Show', backref=db.backref('artist', lazy=True))

    def __repr__(self):
        return f'<Venue {self.city} {self.state} {self.name} {self.id}>'




class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(120), nullable=True, default = " ")

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state}>'