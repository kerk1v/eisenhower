from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Matrix views
    path('', views.MatrixView.as_view(), name='matrix'),
    path('task/new/', views.TaskCreate.as_view(), name='task-create'),
    path('task/<int:pk>/edit/', views.TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDelete.as_view(), name='task-delete'),
    path('task/<int:pk>/toggle/', views.toggle_task_completion, name='task-toggle'),
    path('task/<int:pk>/update-quadrant/', views.update_task_quadrant, name='update-task-quadrant'),

    # User management
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/new/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='matrix/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='matrix'), name='logout'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password-change'),
]