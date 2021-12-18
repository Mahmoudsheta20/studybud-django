from django.urls import path
from . import views

urlpatterns = [
    path('', views.geteoutes),
    path('rooms', views.getroom),

]
