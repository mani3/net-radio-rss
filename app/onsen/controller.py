#!/usr/bin/env python
# coding: utf-8

import urllib
import urllib2
import hashlib

from lxml import etree
from datetime import datetime
from flask import Blueprint, request, jsonify, Response
from feedgen.feed import FeedGenerator

from app import app, db
from app.onsen.model import Channel, Item

mod_onsen = Blueprint(
    'onsen', __name__, url_prefix=app.config['URL_PREFIX'] + '/onsen')


@mod_onsen.route('/update', methods=['POST'])
def update():
    file_name = request.form['file_name']
    if file_name is None:
        now = datetime.now()
        if now.isoweekday() > 5:
            return ''
        else:
            file_name = 'regular_{0}'.format(now.isoweekday())

    dom = etree.XML(get_xml(file_name))
    for e in dom.xpath('//program'):
        name = e.find('titleHeader').text
        title = e.find('title').text
        type_cd = e.find('typeCd').text
        image_path = e.find('imagePath').text
        number = e.find('number').text
        personality = e.find('personality').text
        update = e.find('update').text
        file_url = e.find('fileUrlIphone').text
        text = e.find('text').text
        copyright = e.find('copyright').text
        if file_url is not None:
            channel = Channel.query.filter_by(name=name).first()
            if channel is None:
                channel = Channel(name, title, image_path, personality, text, copyright)
                db.session.add(channel)
                db.session.commit()
            else:
                channel.title = title
                channel.set_image_url(image_path)
                channel.personality = personality
                channel.text = text
                channel.copyright = copyright
                db.session.merge(channel)
                db.session.commit()
            item = Item.query.filter_by(file_url=file_url).first()
            if item is None:
                item = Item(channel.id, update, type_cd, number, file_url)
                db.session.add(item)
                db.session.commit()
    return ''

@mod_onsen.route('/xml', methods=['GET'])
def xml():
    items = Item.query.join(Channel, Channel.id == Item.channel_id).add_columns(Item.update, Item.number, Item.file_url, Channel.title, Channel.name, Channel.personality, Channel.text, Channel.copyright, Channel.image_url).order_by(Item.update.desc()).all()
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.link(href='http://www.onsen.ag/', rel='alternate')
    fg.title(u'音泉 for Podcast')
    fg.subtitle(u'音泉 アニメ・ゲーム・声優系ラジオ')
    for item in items:
        fe = fg.add_entry()
        fe.id(item.file_url)
        fe.title(u'[{0}][{1}]{2}'.format(item.update.strftime('%Y/%m/%d'), item.number, item.title))
        fe.description(item.text)
        fe.enclosure(item.file_url, 0, 'audio/mpeg')
    xml = fg.rss_str(pretty=True)
    return Response(xml, mimetype='text/xml')

def get_xml(file_name='regular_1'):
    now = datetime.now()
    epoch = now.strftime('%s') + '%03d' % (now.microsecond // 1000)
    url = 'http://onsen.ag/getXML.php?{0}'.format(epoch)
    code = hashlib.md5(now.strftime('%w%d%H')).hexdigest()
    xml = None
    try:
        params = urllib.urlencode({'code':code, 'file_name':file_name})
        headers = {}
        req = urllib2.Request(url, params, headers)
        res = urllib2.urlopen(req)
        xml = res.read()
    except Exception, e:
        raise e
    return xml
