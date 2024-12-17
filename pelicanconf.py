from datetime import datetime

AUTHOR = 'Jean-Christophe Lariviere'
SITENAME = 'jclariviere'
SITEURL = ''

TIMEZONE = 'America/Montreal'
DEFAULT_LANG = 'en'

PATH = 'content'
STATIC_PATHS = ['images', 'css']
ARTICLE_PATHS = ['posts']

# Date and slug in filename
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'
SLUGIFY_SOURCE = 'basename'

# Url settings
ARTICLE_URL = 'posts/{slug}'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

SOCIAL = (('github', 'https://github.com/jclariviere'),
          ('linkedin', 'https://www.linkedin.com/in/jclariviere'))

PLUGINS = []

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

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# --- Theme settings ---

THEME = 'theme-flex'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True
PYGMENTS_STYLE = 'default'
PYGMENTS_STYLE_DARK = 'native'

SITETITLE = "Jean-Christophe Lariviere"
SITESUBTITLE = "Developer | Cybersecurity | DevOps"
SITEDESCRIPTION = "Jean-Christophe Lariviere's blog"
SITELOGO = SITEURL + "/images/glados.jpg"
FAVICON = SITEURL + "/images/favicon.ico"

DISABLE_URL_HASH = True
CUSTOM_CSS = 'css/custom.css'

COPYRIGHT_YEAR = f"2015 - {datetime.now().year}"
COPYRIGHT_NAME = AUTHOR
