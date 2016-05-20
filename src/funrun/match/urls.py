from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.index),
	url(r'^match/$', views.start_match),
	url(r'^match/(?P<match_id>\d+)/$', views.match),
	url(r'^match/(?P<match_id>\d+)/round/$', views.round),
]
