"""patientreport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from.import homepage
urlpatterns = [
    path('admin/', admin.site.urls),
    path('chats/',include('chat.urls')),
    path('personal/',include('chat.urls')),
    path('',homepage.home),
    path('login/',homepage.login),
    path('valid',homepage.valid),
    path('checkmail',homepage.checkmail),
    path('pinvalid',homepage.pinvalid),
    path('changepassword',homepage.changepassword),
    path('aboutus/',homepage.aboutus),
    path('contact/',homepage.contact),
    path('news/',homepage.news),
    path('chat/',homepage.chat),
    path('forget/',homepage.forget),
    path('services/',homepage.services),
    path('hospital/',include('Hospital.urls')),
    path('doctor/',include('Doctor.urls')),
    path('patient/',include('Patient.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)