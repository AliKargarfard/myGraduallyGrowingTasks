from django.test import TestCase, Client
from django.urls import reverse

# from django.utils import timezone

from accounts.models import User, Profile
from todo.models import Task


class TestBlogView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="ali@abc.com", password="Ali@1234", is_active=True
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="Ali",
            last_name="K.",
            description="Ali K. description",
        )
        self.task = Task.objects.create(
            user=self.profile.user,
            task_name="test",
            completed=False,
        )

    def test_todo_list_url_successful_response(self):
        self.client.force_login(self.user)
        url = reverse("todo:task_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(response.content).find("todo"))
        self.assertTemplateUsed(response, template_name="todo/list_tasks.html")

    def test_todo_task_detail_logged_in_response(self):
        self.client.force_login(self.user)
        url = reverse("todo:task_detail", kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_todo_tsk_detail_anonymouse_response(self):
        url = reverse("todo:task_detail", kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
