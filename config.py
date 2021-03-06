# -*- coding: utf-8 -*-
# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database for SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'radio.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Path prefix
URL_PREFIX = '/radio'
