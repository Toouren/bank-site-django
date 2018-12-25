from . import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    url(r'^login$', views.return_login_index, name='login-page'),
    url(r'^moderator$', views.return_moder_index, name='moder-page'),
    path(r'change/<int:id>/', views.process_change, name='change-process'),
    url(r'^register/user$', views.return_user_register_index, name='register-user-page'),
    url(r'^register$', views.return_register_index, name='register-page'),
    url(r'^logout$', views.process_logout, name='logout-process'),
    url(r'^$', views.return_index, name='main-page')
]
