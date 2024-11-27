from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Matrix(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_matrices'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "matrices"
        ordering = ['-created_at']

class MatrixAccess(models.Model):
    matrix = models.ForeignKey(
        Matrix,
        on_delete=models.CASCADE,
        related_name='access_permissions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='matrix_accesses'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "matrix accesses"
        unique_together = ['matrix', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.matrix.title}"

class Task(models.Model):
    matrix = models.ForeignKey(
        Matrix,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,  # Temporarily allow null
        blank=True  # Temporarily allow blank
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_urgent = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    def __str__(self):
        return self.title

    def get_quadrant(self):
        if self.is_urgent and self.is_important:
            return "Do First"
        elif self.is_important and not self.is_urgent:
            return "Schedule"
        elif self.is_urgent and not self.is_important:
            return "Delegate"
        else:
            return "Don't Do"

    class Meta:
        ordering = ['due_date', '-created_at']