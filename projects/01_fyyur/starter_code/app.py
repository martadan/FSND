# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #


import json
import datetime as dt
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import VenueForm, ArtistForm, ShowForm


# ---------------------------------------------------------------------------- #
# App Config.
# ---------------------------------------------------------------------------- #


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ---------------------------------------------------------------------------- #
# Models.
# ---------------------------------------------------------------------------- #


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue_show', lazy=True)

    def __repr__(self):
        return f'<Venue #{self.id}: {self.name}>'


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(255))
    shows = db.relationship('Show', backref='artist_show', lazy=True)

    def __repr__(self):
        return f'<Artist #{self.id}: {self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Show #{self.id}: artist {self.artist_id} at venue {self.venue_id} on {self.start_time}>'


# ---------------------------------------------------------------------------- #
# Filters.
# ---------------------------------------------------------------------------- #


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ---------------------------------------------------------------------------- #
# Controllers.
# ---------------------------------------------------------------------------- #


@app.route('/')
def index():
    return render_template('pages/home.html')


# Venues
# ----------------------------------------------------------------


@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    # TODO - figure out how to best group by city first
    # num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "city": "San Francisco",
        "state": "CA",
        "venues": [{
            "id": 1,
            "name": "The Musical Hop",
            "num_upcoming_shows": 0,
        }, {
            "id": 3,
            "name": "Park Square Live Music & Coffee",
            "num_upcoming_shows": 1,
        }]
    }, {
        "city": "New York",
        "state": "NY",
        "venues": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }]
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_string = request.form.get('search_term', '')
    filtered_query = Venue.query.filter(Venue.name.ilike('%' + search_string + '%'))
    venue_count = filtered_query.count()
    data = filtered_query.all()
    # adding num_upcoming_shows, even though it looks like form doesn't use it
    for venue in data:
        venue.num_upcoming_shows = \
            Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time > dt.datetime.now()).count()
    response = {
        "count": venue_count,
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_string)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    data = Venue.query.get(venue_id)

    # add past shows, convert datetime to string, add renamed variables for joined data
    data.past_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time < dt.datetime.now()).join(Artist)
    for show in data.past_shows:
        show.start_time = dt.datetime.strftime(show.start_time, format='%Y-%m-%d %H:%M')
        show.artist_name = show.artist_show.name
        show.artist_image_link = show.artist_show.image_link

    data.upcoming_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time > dt.datetime.now()).join(Artist)
    for show in data.upcoming_shows:
        show.start_time = dt.datetime.strftime(show.start_time, format='%Y-%m-%d %H:%M')
        show.artist_name = show.artist_show.name
        show.artist_image_link = show.artist_show.image_link

    return render_template('pages/show_venue.html', venue=data)


# Create Venue
# ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    new_venue = Venue(
        name=request.form['name'],
        city=request.form['city'],
        state=request.form['state'],
        address=request.form['address'],
        phone=request.form['phone'],
        # image_link=request.form['image_link'],
        facebook_link=request.form['facebook_link']
    )

    try:
        db.session.add(new_venue)
        db.session.commit()
        flash('Venue ' + new_venue.name + ' was successfully listed!')
    except:
        flash('An error occurred. Venue ' + new_venue.name + ' could not be listed.')
    finally:
        return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.get(venue_id).delete()
        db.session.commit()
        flash('Venue id ' + venue_id + ' was successfully deleted!')
    except:
        flash('Error! Venue id ' + venue_id + ' was not deleted!')
    finally:
        return render_template('pages/home.html')
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    # return None


# Artists
# ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_string = request.form.get('search_term', '')
    filtered_query = Artist.query.filter(Artist.name.ilike('%' + search_string + '%'))
    artist_count = filtered_query.count()
    data = filtered_query.all()
    # adding num_upcoming_shows, even though it looks like form doesn't use it
    for artist in data:
        artist.num_upcoming_shows = \
            Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time > dt.datetime.now()).count()
    response = {
        "count": artist_count,
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    data = Artist.query.get(artist_id)
    try:
        data.genres = data.genres.split(',')
    except:
        print('Could not split list of genres')
    return render_template('pages/show_artist.html', artist=data)


# Update
# ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO figure out how to change genres
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form['genres']
    artist.facebook_link = request.form['facebook_link']

    try:
        db.session.commit()
        flash('Artist ' + artist.name + ' was successfully updated!')
    except:
        flash('An error occurred. Artist ' + artist.name + ' was not updated!')
    finally:
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    # venue.genres = request.form['genres']
    venue.facebook_link = request.form['facebook_link']

    try:
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully updated!')
    except:
        flash('An error occurred. Venue ' + venue.name + ' was not updated!')
    finally:
        return redirect(url_for('show_venue', venue_id=venue_id))


# Create Artist
# ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO fix how 'genres' writes
    print(request.form['genres'], flush=True)
    new_artist = Artist(
        name=request.form['name'],
        city=request.form['city'],
        state=request.form['state'],
        phone=request.form['phone'],
        genres=request.form['genres'],
        facebook_link=request.form['facebook_link'],
    )
    try:
        db.session.add(new_artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + new_artist.name + ' was successfully listed!')
    except:
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')
    finally:
        return render_template('pages/home.html')


# Shows
# ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows

    data = Show.query.outerjoin(Artist).outerjoin(Venue)
    for show in data:
        show.start_time = dt.datetime.strftime(show.start_time, format='%Y-%m-%d %H:%M')
        show.venue_name = show.venue_show.name
        show.artist_name = show.artist_show.name
        show.artist_image_link = show.artist_show.image_link
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # insert form data as a new Show record in the db
    new_show = Show(
        artist_id=request.form['artist_id'],
        venue_id=request.form['venue_id'],
        start_time=request.form['start_time']
    )
    try:
        db.session.add(new_show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    finally:
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


# ---------------------------------------------------------------------------- #
# Launch.
# ---------------------------------------------------------------------------- #


# Default port:
if __name__ == '__main__':
    app.run()
    # data = Show.query.outerjoin(Artist).outerjoin(Venue)
    # for show in data:
    #     print(show.)
    # print()
    # AAA = Venue.query.outerjoin(Show).all()
    # print(AAA)
    # for venue_num in AAA:
    #     print(venue_num)
    #     venue_num.num_upcoming_shows = 0
    #     for venue_show in venue_num.shows:
    #         if venue_show.start_time > dt.datetime.today():
    #             venue_num.num_upcoming_shows += 1
    # print(AAA)
    # print()


# Or specify port manually:
'''
if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
'''
