from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .models import Matrix, Task, MatrixAccess
from datetime import datetime, timedelta

class ModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        
        # Create test matrix
        self.matrix = Matrix.objects.create(
            title="Test Matrix",
            description="Test Description",
            owner=self.user1
        )
        
        # Create test task
        self.task = Task.objects.create(
            matrix=self.matrix,
            title="Test Task",
            description="Test Description",
            is_urgent=True,
            is_important=True,
            created_by=self.user1
        )

    def test_matrix_creation(self):
        """Test matrix creation and string representation"""
        self.assertEqual(str(self.matrix), "Test Matrix")
        self.assertEqual(self.matrix.owner, self.user1)
        self.assertTrue(isinstance(self.matrix.created_at, datetime))

    def test_task_creation(self):
        """Test task creation and string representation"""
        self.assertEqual(str(self.task), "Test Task")
        self.assertEqual(self.task.matrix, self.matrix)
        self.assertEqual(self.task.created_by, self.user1)

    def test_task_quadrant(self):
        """Test task quadrant logic"""
        # Test "Do First" quadrant
        self.assertEqual(self.task.get_quadrant(), "Do First")
        
        # Test "Schedule" quadrant
        self.task.is_urgent = False
        self.task.is_important = True
        self.task.save()
        self.assertEqual(self.task.get_quadrant(), "Schedule")
        
        # Test "Delegate" quadrant
        self.task.is_urgent = True
        self.task.is_important = False
        self.task.save()
        self.assertEqual(self.task.get_quadrant(), "Delegate")
        
        # Test "Don't Do" quadrant
        self.task.is_urgent = False
        self.task.is_important = False
        self.task.save()
        self.assertEqual(self.task.get_quadrant(), "Don't Do")

    def test_matrix_access(self):
        """Test matrix access creation and constraints"""
        # Create matrix access
        access = MatrixAccess.objects.create(matrix=self.matrix, user=self.user2)
        self.assertEqual(str(access), f"{self.user2.username} - {self.matrix.title}")
        
        # Test unique constraint
        with self.assertRaises(Exception):
            MatrixAccess.objects.create(matrix=self.matrix, user=self.user2)

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create users
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin_user = User.objects.create_user(username='admin', password='admin123')
        
        # Create admin group and add admin user to it
        self.admin_group = Group.objects.create(name='admins')
        self.admin_user.groups.add(self.admin_group)
        
        # Create test matrix
        self.matrix = Matrix.objects.create(
            title="Test Matrix",
            description="Test Description",
            owner=self.user
        )

    def test_matrix_view_authentication(self):
        """Test matrix view requires authentication"""
        response = self.client.get(reverse('matrix'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
        
        # Test authenticated access
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('matrix'))
        self.assertEqual(response.status_code, 200)

    def test_task_crud(self):
        """Test task CRUD operations"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create task
        response = self.client.post(reverse('task-create'), {
            'title': 'New Task',
            'description': 'New Description',
            'matrix': self.matrix.id,
            'is_urgent': True,
            'is_important': True
        })
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        
        # Read task
        response = self.client.get(reverse('task-view', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        
        # Update task
        response = self.client.post(reverse('task-update', args=[task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'matrix': self.matrix.id,
            'is_urgent': False,
            'is_important': True
        })
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')
        
        # Delete task
        response = self.client.post(reverse('task-delete', args=[task.id]))
        self.assertEqual(Task.objects.count(), 0)

    def test_matrix_sharing(self):
        """Test matrix sharing functionality"""
        self.client.login(username='testuser', password='testpass123')
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        
        # Share matrix
        response = self.client.post(reverse('matrix-share', args=[self.matrix.id]), {
            'user_id': user2.id
        })
        self.assertTrue(MatrixAccess.objects.filter(matrix=self.matrix, user=user2).exists())
        
        # Revoke access
        response = self.client.post(reverse('matrix-revoke', args=[self.matrix.id, user2.id]))
        self.assertFalse(MatrixAccess.objects.filter(matrix=self.matrix, user=user2).exists())

    def test_admin_required_views(self):
        """Test admin-required views"""
        # Test with normal user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 302)  # Redirects due to lack of permission
        
        # Test with admin user
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)

class TaskQuadrantTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.matrix = Matrix.objects.create(
            title="Test Matrix",
            description="Test Description",
            owner=self.user
        )
        self.client.login(username='testuser', password='testpass123')

    def test_update_task_quadrant(self):
        """Test updating task quadrant via API"""
        task = Task.objects.create(
            matrix=self.matrix,
            title="Test Task",
            description="Test Description",
            is_urgent=False,
            is_important=False,
            created_by=self.user
        )
        
        # Test moving to each quadrant
        quadrants = {
            'do_first': {'is_urgent': True, 'is_important': True},
            'schedule': {'is_urgent': False, 'is_important': True},
            'delegate': {'is_urgent': True, 'is_important': False},
            'dont_do': {'is_urgent': False, 'is_important': False}
        }
        
        for quadrant, expected in quadrants.items():
            response = self.client.post(reverse('update-task-quadrant', args=[task.id]), {
                'quadrant': quadrant
            })
            self.assertEqual(response.status_code, 200)
            task.refresh_from_db()
            self.assertEqual(task.is_urgent, expected['is_urgent'])
            self.assertEqual(task.is_important, expected['is_important'])

    def test_toggle_task_completion(self):
        """Test toggling task completion status"""
        task = Task.objects.create(
            matrix=self.matrix,
            title="Test Task",
            description="Test Description",
            is_urgent=True,
            is_important=True,
            created_by=self.user
        )
        
        # Test marking as complete
        response = self.client.post(reverse('task-toggle', args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.completed)
        
        # Test marking as incomplete
        response = self.client.post(reverse('task-toggle', args=[task.id]))
        task.refresh_from_db()
        self.assertFalse(task.completed)