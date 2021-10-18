from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('create/',views.create,name="create"),
    path('<str:query>/',views.treelink,name="treelink"),
    path('editree/<str:no>',views.edittree,name="editree"),
    path('deletree/<str:no>',views.deletree,name="deletree")
]
