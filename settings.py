# Django settings for LoseIt (loseit) project.
# Auto generated on Thu 05 Nov 2015 06:13:32 AM  for PyPE version 27.8.0

import os
import posixpath

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

############################################################################
# !!! Important! These settings should be for development only.
# !!! Edit the project settings online to add your debug settings.
# !!! These settings will be overwritten on the utdirect servers.
DEBUG = True
############################################################################

############################################################################
# PYPE settings

# The default service to use when calling broker.
PYPE_SERVICE = 'TEST'

# Directory to use for temporary files.  You can change this to something 
# valid on your workstation for developing locally.
PYPE_TEMP_DIR = '/tmp'
############################################################################


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

############################################################################
# !!! Important! These settings should be for development only.
# !!! Edit the project settings online to add your database settings.
# !!! These settings will be overwritten on the utdirect servers.
DATABASES = {
    'default': {
        'ENGINE': '',          # 'django.db.backends.mysql' or
                               # 'django.db.backends.oracle' or
                               # 'django.db.backends.sqlite3'  
        'NAME': '',            # Or path to database file if using sqlite3.
        'USER': '',            # Not used with sqlite3.
        'PASSWORD': '',        # Not used with sqlite3.
        'HOST': '',            # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',            # Set to empty string for default. Not used with sqlite3.
    }
}
############################################################################

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds static content such as
# images, css, and javascript files.
# Example: "/home/media/media.lawrence.com/"
STATIC_ROOT = os.path.join(CURRENT_DIR, 'static', '')

# URL that handles the media served from STATIC_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com", "http://example.com/media/"
STATIC_URL = '/apps/user_js52443/loseit/static/'

# MEDIA_ROOT and MEDIA_URL are intended for user-uploaded files. Since
# Pype doesn't have this capacity yet, they are set to None.
MEDIA_ROOT = None
MEDIA_URL = None

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qazd&amp;d_0fqp2o32dsq%whgbr8i7@9!^wq&amp;!vy!41+zvju00&amp;^-'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'utdirect.middleware.HttpHeaderMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'user_js52443.loseit.urls'

# These are hosts allowed to access your server.  This will be
# overwritten on the Pype servers with the appropriate utdirect
# servers.
ALLOWED_HOSTS = ['local.utexas.edu',]

# This is the amount of time, in seconds, that Django will leave DB
# connections open.  600 is enforced on the servers.
CONN_MAX_AGE = 600

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            # Don't forget to use absolute paths, not relative paths.
            os.path.join(CURRENT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    'utdirect',
    # Add your apps created with 'python manage.py my_app':
    # 'user_js52443.loseit.my_app'
)
