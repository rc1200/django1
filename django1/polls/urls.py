from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # the Name is the name of the Python Function to run and can return the HTTP response
]