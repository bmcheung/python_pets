from django.conf.urls import url
from . import views


app_name = 'pets'
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^register$', views.Register.as_view(), name='register'),
    url(r'^map$', views.Map, name='map'),
    url(r'^adopt$', views.Adopt, name='adopt'),
    url(r'^lost$', views.Lost, name='lost'),
    url(r'^found$', views.Found, name='found'),
    url(r'^about$', views.About, name='about'),
    url(r'^logout$', views.Log_out, name='logout'),
]
