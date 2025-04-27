from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from todo.views import ListTask,CreateTask,TaskDetailView
# Create your tests here.

class TestUrl(SimpleTestCase):

    def test_task_list_url_resolve(self):
        url = reverse('todo:list_tasks')
        self.assertEqual(resolve(url).func.view_class,ListTask)

    def test_task_create_url_resolve(self):
        url = reverse('todo:create_task')
        self.assertEqual(resolve(url).func.view_class,CreateTask)

    def test_task_detail_url_resolve(self):
        url = reverse('todo:task_detail',kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class,TaskDetailView)

