from django.conf.urls import url
from authentication import views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^create-user', views.create_user, name='create-user'),
    url(r'^change-password', views.change_password, name='change-password'),
    url(r'^logout', views.logout, name='logout'),
]
