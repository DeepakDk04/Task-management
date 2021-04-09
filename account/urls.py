
from django.urls import path

from . import views

urlpatterns = [

    path('home/', views.home, name='acc-home'),
    path('register/', views.register, name='acc-register'),
    path('login/', views.loginUser, name='acc-login'),
    path('logout/', views.logoutUser, name='acc-logout'),
    path('profile/', views.profileSetting, name='acc-profileset'),
    path('users-stat/', views.usersStat, name='users-stat'),
    path('user-detail/<str:user_id>', views.userDetail, name='user-detail'),

]
