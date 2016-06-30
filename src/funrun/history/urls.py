from django.conf.urls import url

from . import views


app_name = 'history'

urlpatterns = [
	url(r'^$', views.sheets, name='sheets'),
	url(r'^sheet/(?P<sheet_id>\d+)/$', views.sheet, name='sheet'),
]
