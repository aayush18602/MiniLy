from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('register/',views.Register,name="register"),
    path('login/',views.Login,name="login"),
    path('logout/',views.Logout,name="logout"),
    path('dashboard/',views.Dashboard,name="dashboard"),
    path('generate/',views.generate,name="generate"),
    path('<str:query>',views.home,name="home"),
    path('editly/<str:no>/',views.edit_minily,name="editly"),
    path('deletely/<str:no>',views.deletely,name="deletely")
]

