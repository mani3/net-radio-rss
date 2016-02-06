#!/usr/bin/env python
# coding: utf-8

from urlparse import urlparse, urljoin
from datetime import datetime

from app import app, db

ONSEN_BASE = 'http://www.onsen.ag/'

class Channel(db.Model):
    __tablename__ = 'onsen_channel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    title = db.Column(db.String(256))
    image_url = db.Column(db.String(256))
    personality = db.Column(db.String(128))
    text = db.Column(db.Text)
    copyright = db.Column(db.String(128))

    created_at = db.Column(db.DateTime, default=db.func.localtimestamp())
    updated_at = db.Column(db.DateTime, default=db.func.localtimestamp(), onupdate=db.func.localtimestamp())

    def __init__(self, name, title, image_url, personality, text, copyright):
        self.name = name
        self.title = title
        self.personality = personality
        self.text = text
        self.copyright = copyright
        self.set_image_url(image_url)

    def __repr__(self):
        return u'<{0}({1}, {2})>'.format(self.__class__.__name__, self.name, self.title)

    def set_image_url(self, image_url):
        url = urlparse(image_url)
        if url.hostname is None:
            self.image_url = urljoin(ONSEN_BASE, image_url)
        else:
            self.image_url = image_url


class Item(db.Model):
    __tablename__ = 'onsen_item'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('onsen_channel.id'), nullable=False)
    update = db.Column(db.DateTime)
    type_cd = db.Column(db.Integer, default=1)
    number = db.Column(db.Integer, nullable=False)
    file_url = db.Column(db.String(256), unique=True, nullable=False, )

    created_at = db.Column(db.DateTime, default=db.func.localtimestamp())
    updated_at = db.Column(db.DateTime, default=db.func.localtimestamp(), onupdate=db.func.localtimestamp())

    def __init__(self, channel_id, update, type_cd, number, file_url):
        self.channel_id = channel_id
        self.number = number
        self.type_cd = type_cd
        self.file_url = file_url
        self.update = self.publish_at(update)

    def __repr__(self):
        return u'<{0}({1}, {2}, {3})>'.format(self.__class__.__name__, self.channel_id, self.number, self.file_url)

    def publish_at(self, update):
        now = datetime.now()
        date = update.split('/')
        month = int(date[0]) if date[0] is not None else now.month
        day =  int(date[1]) if date[1] is not None else now.day
        year = now.year
        if month > now.month:
            year = now.year - 1
        return datetime(year, month, day)
