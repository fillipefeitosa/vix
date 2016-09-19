"""Module with app urls."""
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
import vix


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/', login_required(vix.views.task_list), name='list'),
    url(r'^about/', vix.views.about, name='about')
]
