from django.conf.urls import url

from . import views


app_name = 'history'

urlpatterns = [
	url('^$', views.sheets, name='sheets'),
]
