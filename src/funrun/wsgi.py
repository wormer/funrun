"""
Expose the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangofunrun.com/en/1.8/howto/deployment/wsgi/
"""

# noinspection PyUnresolvedReferences
import manage  # set DJANGO_SETTINGS_MODULE

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
