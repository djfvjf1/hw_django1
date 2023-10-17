from django.contrib.auth.models import Group, User
from django.db import models

assigned_group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
resolved_group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

class Problem(models.Model):
    assigned_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_problems')
    resolved_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='resolved_problems')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=15)
    description = models.TextField()
    priority_choices = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    priority = models.CharField(max_length=10, choices=priority_choices)
    resolved_problems = [
        ('resolved', 'решено'),
        ('not resolved', 'не решено'),
    ]
    resolved = models.CharField(max_length=20, choices=resolved_problems, default='none')
    created_at = models.DateTimeField(auto_now_add=True)  # Поле даты создания

    def __str__(self):
        return self.name