#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://postgres:adam@localhost:5432/fyyurdb'


# disable Flask-SQLAlchemy from tracking modifications of objects and emit signals
SQLALCHEMY_TRACK_MODIFICATIONS = False