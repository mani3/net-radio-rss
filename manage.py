#!/usr/bin/env python
# coding: utf-8

import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    '''
    usage:
    if [ ! -d "migrations" ]; then
        python manage.py db init
    fi
    python manage.py db migrate -m "`date '+%Y%m%d%H%M'`"
    python manage.py db show
    python manage.py db upgrade
    '''
    manager.run()

