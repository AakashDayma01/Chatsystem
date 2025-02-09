from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name = 'login'),
    path('logout/', views.logoutuser, name = 'logout'),
    path('register/', views.registeruser, name = 'register'),
    path("",views.home,name="Home"),
    path("room/<str:pk>/",views.room,name="Room"),
    path('profile/<str:pk>/',views.userprofile,name='user-profile'),
    path("create-room/",views.createroom,name="create-room"),
    path("update-room/<str:pk>/",views.updateroom,name="update-room"),
    path("delete-room/<str:pk>/",views.deleteroom,name="delete-room"),
    path("delete-message/<str:pk>/",views.deletemessage,name="delete-message"),
    path('delete-profile/<str:pk>/',views.deleteprofile , name="delete-profile"),
    path("Update-profile/<str:pk>/",views.UpdateProfile,name ="update-profile")
]
