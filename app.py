#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This is the Main file which start the app
#The default encoding for python3 code is utf-8 but
#i will add these comments just in case we need it with Arabic writing


#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import babel
from flask import Flask
from flask_moment import Moment
import dateutil.parser
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

#For Arabic writing using
app.config['JSON_AS_ASCII'] = False

#Set paths to upload folder
# app.config["UPLOADS"] = 'static/uploads'
# UPLOAD_FOLDER = 'static'
# ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

from routes import *



#----------------------------------------------------------------------------#
# Error handler.
#----------------------------------------------------------------------------#


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
