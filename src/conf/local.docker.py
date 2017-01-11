# Used in docker as local.py

from funrun.settings import *

if env('DOKKU_APP_TYPE', None):
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
