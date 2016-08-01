from django.conf.urls import url

from . import views


app_name = 'match'

urlpatterns = [
	url(r'^$', views.index, name='root'),
	url(r'^match/$', views.start_match, name='start_match'),
	url(r'^match/(?P<match_id>\d+)/$', views.match, name='match'),
	url(r'^match/(?P<match_id>\d+)/round/$', views.round, name='round'),
	url(r'^stats/$', views.month_stats, name='month_stats'),
]
