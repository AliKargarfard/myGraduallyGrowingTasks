from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="abc@abc.com", password="ali@1234", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTaskApi:
    def test_get_Task_response_200_status(self, api_client):
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
        data = {
            "task_name": "First",
            "completed": False,
        }
        user = common_user
        print(user)
        assert user.is_authenticated  # True
        assert user.is_verified  # True

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data, format="json")
        print(response.__dict__, "\n***************\n", api_client.__dict__)

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
