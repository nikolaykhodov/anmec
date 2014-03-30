# -*- coding: utf-8 -*-

import os


###########
### GLOBAL
###########

DEBUG = os.environ.get('ENABLE_DEBUG') == '1'

ROOT_DIR = os.path.dirname(__file__)

######################
### UPDATING SETTINGS
######################

UPDATER_SLEEP_TIME = 60.0

# Host that is used for collecting the groups data
# If host is empty string, the collecting will be executed on local machine

UPDATING_GROUPS_HOST = 'collector.domain.com'
#UPDATING_GROUPS_HOST = ''

# Username[:password] for host that is being used for collecting the groups data
UPDATING_GROUPS_USER = 'collector'

#
UPDATING_GROUPS_COUNT = 55617977

UPDATING_GROUPS_MIN_PEOPLE = 1000

# Host that is used for collecting the stat data
# If host is empty string, the collecting will be executed on local machine

UPDATING_ANALYTICS_HOST = 'collector.domain.com'
#UPDATING_ANALYTICS_HOST = ''

# User[:password] for host that is being used for collecting the stat data
UPDATING_ANALYTICS_USER = 'collector:xxx'

# Host that is used for collecting the stat data
# If host is empty string, the collecting will be executed on local machine

UPDATING_POSTS_HOST = 'collector.domain.com'
#UPDATING_POSTS_HOST = ''

# User[:password] for host that is being used for collecting the stat data
UPDATING_POSTS_USER = 'collector:xxx'

# Delay between two subsequent feeding
UPDATING_POSTS_DELAY = 0.2

# Job trackers for each type of collecting
UPDATING_TRACKERS = {
    'groups': 'https://script.google.com/macros/s/AKfycbw1BKMuxSAzjZeyxp-0KGjXC5CahdYXBL4bA0sjv4U5tVdu6b4/exec',
    'analytics': 'https://script.google.com/macros/s/AKfycbw1BKMuxSAzjZeyxp-0KGjXC5CahdYXBL4bA0sjv4U5tVdu6b4/exec',
    'posts': 'https://script.google.com/macros/s/AKfycbw1BKMuxSAzjZeyxp-0KGjXC5CahdYXBL4bA0sjv4U5tVdu6b4/exec'
}

UPDATING_POSTS_TOP_GROUPS = 100
##################
### DJANGO SETTINGS
#################

import os
import sys

DJANGO_ROOT_DIR = os.path.join(os.path.dirname(__file__), 'server/src/')
p = lambda path: os.path.join(DJANGO_ROOT_DIR, path)
sys.path.insert(0, p('.'))
sys.path.insert(0, p('libs'))


TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'admin@domain.com'),
)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'anmec2',                      # Or path to database file if using sqlite3.
        'USER': 'anmec2',                      # Not used with sqlite3.
        'PASSWORD': 'password',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wkpf0p_)5(+n6kfz#qk))osx@6opohqjdo8_g0mri&amp;ce#(j(7x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account.auth.AccountBackend',
)

ROOT_URLCONF = 'server.src.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'server.src.wsgi.application'

TEMPLATE_DIRS = (
    p('templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.admin',

    'gunicorn',
    'south',
    'corsheaders',
    'jsonforms',
    'pg_introspection',
    'anmec_utils',

    'search',
    'account',
)
CORS_ORIGIN_WHITELIST = (
    'localhost',
)
CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = ['app.domain.com']

# How many rows are seen at search results page
RESULTS_PER_PAGE = 20

SECURE_LINK_SECRET = 't8saj4kew21JW2ddb6ZrnSirjCm24ehf'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': p('error.log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

SPHINX_SERVER = 'localhost'
SPHINX_PORT = 3312
SPHINX_GROUPS_INDEX = 'anmec2_groups'
SPHINX_POSTS_INDEX = 'anmec2_posts'
SPHINX_MAXMATCHES = 100000
SPHINX_MIN_LENGTH = 4

VK_APP_ID = '2836076'
VK_APP_KEY = 'B5Yu9GxyWrrm2CNBMu'

if os.environ.get('DEVELOPMENT') == '1':
    from  settings_dev import *
    import logging
    logging.basicConfig(level=logging.DEBUG)

if 'test' in sys.argv:
    SOUTH_TESTS_MIGRATE = False

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': p('test_sqlite.db')
        }
    }

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
        'django.contrib.auth.hashers.SHA1PasswordHasher',
    )
