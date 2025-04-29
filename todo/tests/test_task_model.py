from django.test import TestCase

# from django.utils import timezone

from todo.models import Task
from accounts.models import User, Profile


class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@abc.com", password="Ali@1234")
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="test_first_name",
            last_name="test_last_name",
            description="test Bio description",
        )

    def test_create_task_with_valid_data(self):

        task = Task.objects.create(
            user=self.profile.user,
            task_name="test Task",
            completed=False,
        )
        self.assertTrue(Task.objects.filter(pk=task.id).exists())
        self.assertEqual(task.task_name, "test Task")
