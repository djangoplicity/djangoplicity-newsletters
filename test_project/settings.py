"""
Django settings for test project.

Generated by 'django-admin startproject' using Django 1.11.21.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# We can't use ugettext from django.utils.translation as it will itself
# load the settings resulting in a ImproperlyConfigured error
ugettext = lambda s: s

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(BASE_DIR, 'tmp')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')o0n4t(00@de#j2h77p%3u#t$vfpg266nwdb42kw%q9ca283!0'

SHORT_NAME = 'newsletters'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SHARED_DIR = "%s/shared" % BASE_DIR

SITE_ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.redirects',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

DJANGOPLICITY_APPS = [
    'djangoplicity',
    'djangoplicity.menus',
    'djangoplicity.reports',
    'djangoplicity.pages',
    'djangoplicity.media',
    'djangoplicity.archives',
    'djangoplicity.archives.contrib.security',
    'djangoplicity.announcements',
    'djangoplicity.science',
    'djangoplicity.releases',
    'djangoplicity.metadata',
    'djangoplicity.adminhistory',
    'djangoplicity.utils',
    'djangoplicity.celery',
    'djangoplicity.mailinglists',
    'djangoplicity.newsletters',
    'djangoplicity.iframe',
    'djangoplicity.admincomments',
    'djangoplicity.simplearchives',
    'djangoplicity.actions',
    'djangoplicity.cutter',
]

THIRD_PARTY_APPS = [
    'test_project',
    'django_mailman',
    'tinymce'
]

INSTALLED_APPS = DJANGO_APPS + DJANGOPLICITY_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'test_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'test_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangoplicity-newsletters',
        'USER': 'djangoplicity-newsletters',
        'PASSWORD': 'djangoplicity-newsletters',
        'HOST': 'djangoplicity-newsletters-db',
        'PORT': '5432',
    }
}

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'djangoplicity-newsletters',
            'USER': 'djangoplicity-newsletters',
            'PASSWORD': 'djangoplicity-newsletters',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# For static media protection to be enabled, and archive must be present here
# For file import to work, the archive must be present here.
ARCHIVES = (
    ('djangoplicity.media.models.Image', 'djangoplicity.media.options.ImageOptions'),
    ('djangoplicity.media.models.Video', 'djangoplicity.media.options.VideoOptions'),
    ('djangoplicity.media.models.VideoSubtitle', 'djangoplicity.media.options.VideoSubtitleOptions'),
    ('djangoplicity.media.models.ImageComparison', 'djangoplicity.media.options.ImageComparisonOptions'),
    ('djangoplicity.releases.models.Release', 'djangoplicity.releases.options.ReleaseOptions'),
    ('djangoplicity.announcements.models.Announcement','djangoplicity.announcements.options.AnnouncementOptions'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGES = (
    ('en', ugettext('English')),
)

LANGUAGE_CODE = 'en'

SITE_ID = 1

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

##############
# JavaScript #
##############
JQUERY_JS = "jquery/jquery-1.11.1.min.js"
JQUERY_UI_JS = "jquery-ui-1.12.1/jquery-ui.min.js"
JQUERY_UI_CSS = "jquery-ui-1.12.1/jquery-ui.min.css"
DJANGOPLICITY_ADMIN_CSS = "djangoplicity/css/admin.css"
DJANGOPLICITY_ADMIN_JS = "djangoplicity/js/admin.js"
SUBJECT_CATEGORY_CSS = "djangoplicity/css/widgets.css"

ARCHIVE_AUTO_RESOURCE_DELETION = False
RELEASE_ARCHIVE_ROOT = 'archives/releases/'
IMAGES_ARCHIVE_ROOT = 'archives/images/'
IMAGECOMPARISON_ARCHIVE_ROOT = 'archives/imagecomparisons/'
VIDEOS_ARCHIVE_ROOT = 'archives/videos/'
ANNOUNCEMENTS_ARCHIVE_ROOT = 'archives/announcements/'
NEWSLETTERS_ARCHIVE_ROOT = 'archives/newsletters/'
SCIENCEANNOUNCEMENTS_ARCHIVE_ROOT = 'archives/science/'


NEWSLETTERS_MAILCHIMP_API_KEY = os.environ.get("NEWSLETTERS_MAILCHIMP_API_KEY")
NEWSLETTERS_MAILCHIMP_LIST_ID = os.environ.get("NEWSLETTERS_MAILCHIMP_LIST_ID")

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
        textcolor save link image media preview codesample table
        code lists fullscreen  insertdatetime  nonbreaking contextmenu
        directionality searchreplace wordcount visualblocks visualchars
        code fullscreen autolink lists  charmap print  hr anchor pagebreak
    ''',
    'toolbar1': '''
        fullscreen code | cut copy | searchreplace | alignleft aligncenter alignright alignjustify | formatselect forecolor backcolor | superscript subscript |
     ''',
    'toolbar2': '''
        bold italic underline strikethrough | bullist numlist table hr | indent outdent | undo redo | link unlink anchor image media charmap | nonbreaking |
    ''',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'statusbar': True,
    'entity_encoding': 'raw',
    'convert_urls': False,
}

ENABLE_ADVANCED_SEARCH = True
ADV_SEARCH_START_YEAR = 1998

# CELERY
CELERY_IMPORTS = [
    "djangoplicity.archives.contrib.security.tasks",
    "djangoplicity.celery.tasks",
]
# Task result backend
CELERY_RESULT_BACKEND = "amqp"
CELERY_BROKER_URL = 'amqp://guest:guest@broker:5672/'
# Avoid infinite wait times and retries
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}
# AMQP backend settings - Required for flower to work as intended
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_EXPIRES = 3600
# File to save revoked tasks across workers restart
CELERY_WORKER_STATE_DB = os.path.join(TMP_DIR, 'celery_states')
CELERY_BEAT_SCHEDULE_FILENAME = os.path.join(TMP_DIR, 'celerybeat_schedule')
