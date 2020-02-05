from.import views
from django.urls import path

urlpatterns = [
    path('',views.index),
    path('home',views.home),
    path('home/',views.loginhospital),
    path('home/upload/',views.upload),
    path('home/view/',views.view),
    path('home/userdata',views.userdata),
    path('home/logout/',views.out),

]