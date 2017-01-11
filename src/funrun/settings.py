import os

from environ import Env as DjangoEnv
from environs import Env

env = Env()
env.add_parser('db_settings', DjangoEnv.db_url_config)
env.add_parser('email_settings', DjangoEnv.email_url_config)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAR_DIR = os.path.join(PROJECT_DIR, 'var')

INSTALLED_APPS = [
	# Rules for this list:
	# - Group apps by module
	# - Sort groups by time (recently added go last)
	# - Sort apps within a group alphabetically
	# - If you need to place an app out of order, leave a comment explaining the reason why.
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.staticfiles',

	'aldjemy',

	'funrun.match',
	'funrun.history',
]

MIDDLEWARE_CLASSES = [
	# Rules for this list:
	# - Django middleware go in default order.
	# - Group apps by module
	# - Sort groups by time (recently added go last)
	# - Sort apps within a group alphabetically
	# - If you need to place an app out of order, leave a comment explaining the reason why.
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'funrun.urls'

WSGI_APPLICATION = 'manage.wsgi_application'

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'ru-ru'

USE_TZ = True
TIME_ZONE = 'America/New_York'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.contrib.auth.context_processors.auth',
			],
		}
	},
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(VAR_DIR, 'static')

STATICFILES_ROOT = os.path.join(PROJECT_DIR, 'static')
STATICFILES_DIRS = [STATICFILES_ROOT]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(VAR_DIR, 'media')

# AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_FROM_EMAIL = 'funrun@wormer.inetss.com'

SERVER_EMAIL = 'wormer@inetss.com'
EMAIL_SUBJECT_PREFIX = '[funrun] '  # for mailing admins and managers

SECRET_KEY = env('SECRET_KEY', None)  # generate a random key with 'pwgen -s 50 -n 1'

DEBUG = env.bool('DEBUG', False)
SENTRY_DSN = env('SENTRY_DSN', None)
if SENTRY_DSN:
	RAVEN_CONFIG = {'dsn': SENTRY_DSN}
	INSTALLED_APPS.insert(0, 'raven.contrib.django.raven_compat')

DATABASES = {
	'default': env.db_settings('DATABASE_URL', 'postgres://localhost/funrun')
}

if env('EMAIL_URL', None):
	vars().update(env.email_settings('EMAIL_URL'))

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])


# Pagination

MATCHES_PER_PAGE = 10


from conf.local import *
