from django.test import SimpleTestCase
from django.urls import reverse, resolve
from todo.views import ListTask

# from accounts.models import User


class TestUrls(SimpleTestCase):

    def test_todo_list_url_resolve(self):
        url = reverse("todo:task_list")
        self.assertEquals(resolve(url).func.view_class, ListTask)
