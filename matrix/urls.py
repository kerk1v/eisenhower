from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Matrix views
    path('', views.MatrixView.as_view(), name='matrix'),
    path('task/new/', views.TaskCreate.as_view(), name='task-create'),
    path('task/<int:pk>/', views.TaskView.as_view(), name='task-view'),
    path('task/<int:pk>/edit/', views.TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDelete.as_view(), name='task-delete'),
    path('task/<int:pk>/toggle/', views.toggle_task_completion, name='task-toggle'),
    path('task/<int:pk>/update-quadrant/', views.update_task_quadrant, name='update-task-quadrant'),

    # Matrix Management
    path('management/', views.MatrixManagementView.as_view(), name='matrix-management'),
    path('matrix/create/', views.create_matrix, name='matrix-create'),
    path('matrix/<int:pk>/edit/', views.MatrixUpdate.as_view(), name='matrix-edit'),
    path('matrix/<int:pk>/delete/', views.MatrixDelete.as_view(), name='matrix-delete'),
    path('matrix/<int:matrix_id>/share/', views.share_matrix, name='matrix-share'),
    path('matrix/<int:matrix_id>/revoke/<int:user_id>/', views.revoke_matrix_access, name='matrix-revoke'),

    # User management
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/new/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='matrix/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='matrix'), name='logout'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password-change'),
]