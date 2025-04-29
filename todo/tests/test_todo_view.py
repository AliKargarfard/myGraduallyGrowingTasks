from django.test import TestCase,Client
from django.urls import reverse
from django.utils import timezone

from accounts.models import User,Profile
from todo.models import Task


class TestTodoView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="ali@abc.com",password="Ali@1234")
        self.profile = Profile.objects.create(
            user=self.user,
            first_name = "Ali",
            last_name = "K.",
            description = "Ali K. description",
        )
        self.task = Task.objects.create(
            user = self.user,
            task_name = "test TASK",
            completed = True,
            published_at = timezone.now()
        )

    
    def test_todo_index_url_successful_response(self):
        url = reverse('todo:list_tasks')
        response = self.client.get(url)
        self.assertTrue(str(response.content).find("list_tasks"))
        self.assertTemplateUsed(response,template_name = "list_tasks.html")
        self.assertEquals(response.status_code, 200)

    # def test_task_complete_logged_in_response(self):
    #     login = self.client.force_login(self.user)
    #     url = reverse('todo:task_done',kwargs={'pk':self.task.id})
    #     response = self.client.get(url)
    #     # print(response.url, '************', self.user ,'.........',self.post.id, '........', url)
    #     self.assertEquals(response.status_code, 200)

    # def test_blog_post_detail_anonymouse_response(self):
    #     url = reverse('blog:post_detail',kwargs={'pk':self.post.id})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    
    