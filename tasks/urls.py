from django.urls import path
from tasks import views


urlpatterns = [
     path('tasks/', views.tasks, name='tasks'),
     path('task/<int:id>/', views.task, name='task'),
     path('upload_file/<int:id>/', views.upload_file, name='upload_file'),
     path('download_file/<int:id>/', views.download_file, name='download_file'),
     path('logout/', views.logout, name ='logout')
]