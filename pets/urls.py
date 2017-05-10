from django.conf.urls import url
from . import views


app_name = 'pets'
urlpatterns = [
    url(r'^', views.Home.as_view(), name='home'),
    url(r'^register$', views.Register, name='register')
]
