from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

''' Task model for creating new tasks for the current user '''
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = "user"

    def __str__(self):
        return self.task_name
    
    def get_absolute_api_url(self):
        return reverse('todo:api-v1:task_detail', kwargs={'pk': self.pk})