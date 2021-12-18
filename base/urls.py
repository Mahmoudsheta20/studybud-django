from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('register/', views.registerpage, name="register"),
    path('deletemessage/<str:pk>/', views.deletemessage, name="deletemessage"),

    path('', views.home, name="home"),

    path('room/<int:pk>/', views.room, name="room"),
    path('profile/<int:pk>/', views.profile, name="profile"),

    path('create-Room/', views.createRoom, name="create_room"),
    path('updateRoom/<str:pk>/', views.updateRoom, name="updateRoom"),
    path('deleteRoom/<str:pk>/', views.deleteRoom, name="deleteRoom"),
    path('updateuser/', views.updateuser, name="updateuser"),
    path('topicpage/', views.topicpage, name="topicpage"),
    path('activpage/', views.activpage, name="activpage"),
]
