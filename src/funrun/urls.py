from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
import django.views.static


admin.autodiscover()

urlpatterns = [
	# robots.txt and friends
	url(r'^([^/]+\.[^/]+)$', django.views.static.serve, {'document_root': settings.STATICFILES_ROOT}),
	url(r'^admin/', include(admin.site.urls)),
	url(r'', include('funrun.match.urls')),
]

if settings.DEBUG and settings.MEDIA_URL.startswith('/'):
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
