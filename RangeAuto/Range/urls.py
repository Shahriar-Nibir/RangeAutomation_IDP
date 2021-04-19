from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginUser, name='login'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('inputfirer', views.inputfirer, name='inputfirer'),
    path('showmember', views.showmember, name='showmember'),
    path('firingresult', views.firingresult, name='firingresult'),
    path('result/<str:pk>', views.result, name='result'),
    path('adddetail', views.adddetail, name='adddetail')
]
