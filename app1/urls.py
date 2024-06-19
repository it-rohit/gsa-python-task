from django.urls import path
from .views import Register,Login,TaskCreate,TaskList

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('tasks/create/', TaskCreate.as_view(), name='create_task'),
    path('tasks/<int:pk>', TaskList.as_view(), name='task_list'),
    
]