from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Task, Matrix, MatrixAccess

class MatrixView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'matrix/matrix.html'
    context_object_name = 'tasks'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get matrices the user has access to
        available_matrices = Matrix.objects.filter(
            Q(owner=user) | Q(access_permissions__user=user)
        ).distinct()

        # Get or set current matrix
        matrix_id = self.request.GET.get('matrix')
        if matrix_id:
            current_matrix = get_object_or_404(available_matrices, id=matrix_id)
        else:
            current_matrix = available_matrices.first()
            if not current_matrix:
                # Create a default matrix for the user if none exists
                current_matrix = Matrix.objects.create(
                    title="My Matrix",
                    owner=user,
                    description="Default matrix"
                )

        tasks = Task.objects.filter(matrix=current_matrix)
        context['current_matrix'] = current_matrix
        context['available_matrices'] = available_matrices
        context['do_first'] = tasks.filter(is_urgent=True, is_important=True, completed=False)
        context['schedule'] = tasks.filter(is_urgent=False, is_important=True, completed=False)
        context['delegate'] = tasks.filter(is_urgent=True, is_important=False, completed=False)
        context['dont_do'] = tasks.filter(is_urgent=False, is_important=False, completed=False)
        context['recent_completed'] = tasks.filter(completed=True).order_by('-id')[:10]
        return context

class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'matrix/task_view.html'
    context_object_name = 'task'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['available_matrices'] = Matrix.objects.filter(
            Q(owner=user) | Q(access_permissions__user=user)
        ).distinct()
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'matrix/task_form.html'
    fields = ['title', 'description', 'matrix', 'is_urgent', 'is_important', 'due_date']
    success_url = reverse_lazy('matrix')
    login_url = 'login'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['matrix'].queryset = Matrix.objects.filter(
            Q(owner=user) | Q(access_permissions__user=user)
        ).distinct()
        return form

    def get_initial(self):
        initial = super().get_initial()
        matrix_id = self.request.GET.get('matrix')
        if matrix_id:
            initial['matrix'] = matrix_id
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse_lazy('matrix')}?matrix={self.object.matrix.id}"

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'matrix/task_form.html'
    fields = ['title', 'description', 'matrix', 'is_urgent', 'is_important', 'due_date', 'completed']
    success_url = reverse_lazy('matrix')
    login_url = 'login'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['matrix'].queryset = Matrix.objects.filter(
            Q(owner=user) | Q(access_permissions__user=user)
        ).distinct()
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse_lazy('matrix')}?matrix={self.object.matrix.id}"

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'matrix/task_confirm_delete.html'
    success_url = reverse_lazy('matrix')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matrix'] = self.object.matrix
        return context

    def delete(self, request, *args, **kwargs):
        matrix_id = self.get_object().matrix.id
        messages.success(self.request, 'Task deleted successfully!')
        response = super().delete(request, *args, **kwargs)
        self.success_url = f"{reverse_lazy('matrix')}?matrix={matrix_id}"
        return response

@login_required(login_url='login')
@require_POST
def toggle_task_completion(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    messages.success(request, f'Task "{task.title}" marked as {"completed" if task.completed else "incomplete"}!')
    return redirect(f"{reverse_lazy('matrix')}?matrix={task.matrix.id}")

@login_required(login_url='login')
@require_POST
@csrf_exempt
def update_task_quadrant(request, pk):
    task = get_object_or_404(Task, pk=pk)
    quadrant = request.POST.get('quadrant')
    
    if quadrant == 'do_first':
        task.is_urgent = True
        task.is_important = True
    elif quadrant == 'schedule':
        task.is_urgent = False
        task.is_important = True
    elif quadrant == 'delegate':
        task.is_urgent = True
        task.is_important = False
    elif quadrant == 'dont_do':
        task.is_urgent = False
        task.is_important = False
    
    task.save()
    return JsonResponse({'status': 'success'})

# Matrix Management Views
class MatrixManagementView(LoginRequiredMixin, ListView):
    model = Matrix
    template_name = 'matrix/matrix_management.html'
    context_object_name = 'owned_matrices'
    login_url = 'login'

    def get_queryset(self):
        return Matrix.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shared_matrices'] = MatrixAccess.objects.filter(user=self.request.user)
        context['available_users'] = User.objects.exclude(id=self.request.user.id)
        return context

@login_required(login_url='login')
@require_POST
def create_matrix(request):
    title = request.POST.get('title')
    description = request.POST.get('description', '')
    
    matrix = Matrix.objects.create(
        title=title,
        description=description,
        owner=request.user
    )
    
    messages.success(request, 'Matrix created successfully!')
    return redirect('matrix-management')

@login_required(login_url='login')
@require_POST
def share_matrix(request, matrix_id):
    matrix = get_object_or_404(Matrix, id=matrix_id, owner=request.user)
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    MatrixAccess.objects.get_or_create(matrix=matrix, user=user)
    messages.success(request, f'Matrix shared with {user.username}!')
    return redirect('matrix-management')

@login_required(login_url='login')
@require_POST
def revoke_matrix_access(request, matrix_id, user_id):
    matrix = get_object_or_404(Matrix, id=matrix_id, owner=request.user)
    MatrixAccess.objects.filter(matrix=matrix, user_id=user_id).delete()
    messages.success(request, 'Access revoked successfully!')
    return redirect('matrix-management')

class MatrixUpdate(LoginRequiredMixin, UpdateView):
    model = Matrix
    template_name = 'matrix/matrix_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('matrix-management')
    login_url = 'login'

    def get_queryset(self):
        return Matrix.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Matrix updated successfully!')
        return super().form_valid(form)

class MatrixDelete(LoginRequiredMixin, DeleteView):
    model = Matrix
    template_name = 'matrix/matrix_confirm_delete.html'
    success_url = reverse_lazy('matrix-management')
    login_url = 'login'

    def get_queryset(self):
        return Matrix.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Matrix deleted successfully!')
        return super().delete(request, *args, **kwargs)

# User Management Views
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='admins').exists()

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('matrix')

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'matrix/user_list.html'
    context_object_name = 'users'
    login_url = 'login'

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'matrix/user_form.html'
    success_url = reverse_lazy('user-list')
    login_url = 'login'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add user to 'users' group by default
        self.object.groups.add(Group.objects.get(name='users'))
        messages.success(self.request, 'User created successfully!')
        return response

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'matrix/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'User deleted successfully!')
        return super().delete(request, *args, **kwargs)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'matrix/password_change.html'
    success_url = reverse_lazy('matrix')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully!')
        return super().form_valid(form)