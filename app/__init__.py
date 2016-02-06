#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path= '/radio/static')
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

@app.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')

from app.onsen.controller import mod_onsen as onsen_module

app.register_blueprint(onsen_module)

db.create_all()
