from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginUser, name='login'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('inputfirer', views.inputfirer, name='inputfirer'),
    path('showmember', views.showmember, name='showmember')
]
