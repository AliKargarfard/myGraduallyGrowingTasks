from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from accounts.models import User, Profile
from todo.models import Task


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="ali@abc.com", password="ali@1234", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTaskApi:


    def setUp(self):
        self.user = User.objects.create_user(email="test@abc.com",password="Ali@1234")
        self.profile = Profile.objects.create(
            user=self.user,
            first_name = "test_first_name",
            last_name = "test_last_name",
            description = "test Bio description",
        )

    def test_get_Task_list_response_200_status(self, api_client):
        url = reverse("todo:api-v1:task_list")
        response = api_client.get(url)
        assert response.status_code == 200


    def test_create_Task_response_403_status(self, api_client):
        url = reverse("todo:api-v1:task_list")
        data = {
            "task_name": "test",
            "completed": True,
        }
        response = api_client.post(url, data)
        assert response.status_code == 403

    def test_create_task_response_201_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task_list")
        user = common_user
        data = {
            "task_name": "First",
            "completed": False,
            "user" : user.id
        }
        print(user)
        assert user.is_authenticated  # True
        assert user.is_verified  # True
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data, format="json")
    
        assert response.status_code == 201

    def test_create_Task_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("todo:api-v1:task_list")
        data = {
            "task_name": "test",
            "completed": True,
        }
        user = common_user

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400


    def test_get_Task_detail_response_200_status(self, api_client, common_user):

        # 1. ساخت تسک تستی
        task = Task.objects.create(
            task_name="Test Task",
            completed=False,
            user= common_user # اختصاص کاربر
            )

        url = reverse('todo:api-v1:task_detail', kwargs={'pk': task.id})
        response = api_client.get(url)
        assert response.status_code == 200        