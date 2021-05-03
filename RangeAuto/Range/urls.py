from django.urls import path, include
from . import views
from ajax_select import urls as ajax_select_urls
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginUser, name='login'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('inputfirer', views.inputfirer, name='inputfirer'),
    path('showmember', views.showmember, name='showmember'),
    path('firingresult', views.firingresult, name='firingresult'),
    path('result/<str:pk>', views.result, name='result'),
    path('adddetail', views.adddetail, name='adddetail'),
    path('invalid', views.invalid, name='invalid'),
    path('compile', views.compile, name='compile'),
    path('tgtimg', views.tgtimg, name='tgtimg')
]
