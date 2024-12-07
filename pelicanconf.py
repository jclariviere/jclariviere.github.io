AUTHOR = 'Jean-Christophe Lariviere'
SITENAME = 'jclariviere'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['images', 'css', 'code']
ARTICLE_PATHS = ['posts']

TIMEZONE = 'America/Montreal'

DEFAULT_LANG = 'en'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['tag_cloud', 'liquid_tags.include_code']

# See this page for defaults: https://docs.getpelican.com/en/latest/settings.html
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight', 'guess_lang': False},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {}, # Adds id attribute to <hX> HTML tags
    },
    'output_format': 'html5',
}

THEME = 'pelican-themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'slate'
CUSTOM_CSS = 'css/custom.css'
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PLUGINS += ['i18n_subsites']

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

TWITTER_CARDS = True
TWITTER_USERNAME = 'jclariviere'

DISPLAY_CATEGORIES_ON_SIDEBAR = True
CATEGORIES_URL = 'categories.html'

DISPLAY_TAGS_ON_SIDEBAR = True
#DISPLAY_TAGS_INLINE = True
TAGS_URL = 'tags.html'
TAG_CLOUD_STEPS = 2
TAG_CLOUD_SORTING = 'alphabetically'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Date and slug in filename
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'
SLUGIFY_SOURCE = 'basename'

# Url settings
ARTICLE_URL = 'posts/{slug}'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

SHOW_DATE_MODIFIED = True
