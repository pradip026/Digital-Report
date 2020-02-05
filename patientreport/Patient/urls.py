from django.urls import path
from.import views

urlpatterns = [
    path('',views.index),
    path('home',views.home),
    path('upload',views.upload),
    path('view',views.view),
    path('post',views.post),
    path('show',views.show),
    path('down',views.down),
    path('home/userdata',views.userdata),
]