from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('task-view/', views.taskViewAll, name='tasks-view'),
    path('task-view/<str:task_id>/', views.taskView, name='task-view'),
    path('task-create/', views.taskCreate, name='task-create'),
    path('task-edit/<str:task_id>/', views.taskEdit, name='task-edit'),
    path('task-delete/<str:task_id>/', views.taskDelete, name='task-delete'),
    path('developercontact/', views.devpCont, name='developercontact'),
    
]
