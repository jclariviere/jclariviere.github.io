#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jean-Christophe Lariviere'
SITENAME = u'jclariviere'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Montreal'

DEFAULT_LANG = u'en'

THEME = 'pelican-bootstrap3'

PLUGIN_PATHS = ['/pelican/pelican-plugins']
PLUGINS = ['tag_cloud']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'https://github.com/jclariviere'),
          ('twitter', 'https://twitter.com/jclariviere'),
          ('linkedin', 'https://www.linkedin.com/in/jclariviere'))

DISPLAY_CATEGORIES_ON_SIDEBAR = True
CATEGORIES_URL = 'categories.html'

DISPLAY_TAGS_ON_SIDEBAR = True
#DISPLAY_TAGS_INLINE = True
TAGS_URL = 'tags.html'
TAG_CLOUD_STEPS = 2
TAG_CLOUD_SORTING = 'alphabetically'


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Date and slug in filename
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'
SLUGIFY_SOURCE = 'basename'

# Url settings
ARTICLE_URL = 'posts/{slug}'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
