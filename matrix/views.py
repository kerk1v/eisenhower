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
from .models import Task

class MatrixView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'matrix/matrix.html'
    context_object_name = 'tasks'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.all()
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

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'matrix/task_form.html'
    fields = ['title', 'description', 'is_urgent', 'is_important', 'due_date']
    success_url = reverse_lazy('matrix')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'matrix/task_form.html'
    fields = ['title', 'description', 'is_urgent', 'is_important', 'due_date', 'completed']
    success_url = reverse_lazy('matrix')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'matrix/task_confirm_delete.html'
    success_url = reverse_lazy('matrix')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required(login_url='login')
@require_POST
def toggle_task_completion(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    messages.success(request, f'Task "{task.title}" marked as {"completed" if task.completed else "incomplete"}!')
    return redirect('matrix')

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