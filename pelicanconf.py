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

# URL settings
ARTICLE_URL = 'blog/post/{slug}/'
CATEGORIES_URL = 'blog/categories/'
CATEGORY_URL = 'blog/category/{slug}/'
TAGS_URL = 'blog/tags/'
TAG_URL = 'blog/tag/{slug}/'
AUTHORS_URL = 'blog/authors/'
AUTHOR_URL = 'blog/author/{slug}/'
ARCHIVES_URL = 'blog/archives/'

# SAVE_AS settings that make the above URLs work
ARTICLE_SAVE_AS = ARTICLE_URL + "index.html"
CATEGORIES_SAVE_AS = CATEGORIES_URL + "index.html"
CATEGORY_SAVE_AS = CATEGORY_URL + "index.html"
TAGS_SAVE_AS = TAGS_URL + "index.html"
TAG_SAVE_AS = TAG_URL + "index.html"
AUTHORS_SAVE_AS = AUTHORS_URL + "index.html"
AUTHOR_SAVE_AS = AUTHOR_URL + "index.html"
ARCHIVES_SAVE_AS = ARCHIVES_URL + "index.html"

LINKS = (
    ('Blog', '/'),
    ('CTF Writeups', 'https://github.com/jclariviere/ctf-writeups'),
)

SOCIAL = (('github', 'https://github.com/jclariviere'),
          ('linkedin', 'https://www.linkedin.com/in/jclariviere'))

PLUGINS = ['pelican.plugins.simple_footnotes']

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
