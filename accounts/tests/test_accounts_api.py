from rest_framework.test import APIClient
from django.urls import reverse
import pytest

# from datetime import datetime
from accounts.models import User, Profile
from todo.models import Task

from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
import pytz


@pytest.fixture
def expired_token(common_user):
    # ساخت یک توکن عادی
    token = AccessToken.for_user(common_user)

    # تغییر زمان انقضا به گذشته (مثلاً ۱ ساعت قبل)
    expired_time = datetime.now(pytz.utc) - timedelta(hours=1)
    token.set_exp(from_time=expired_time)

    return str(token)


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="ali@abc.com", password="ali@1234", is_verified=True, is_active=True
    )
    return user


@pytest.mark.django_db
class TestAccountsApi:

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@abc.com", password="Ali@1234", is_activated=True
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="test_first_name",
            last_name="test_last_name",
            description="test Bio description",
        )

    def test_get_account_registration_correct_statuses(self, api_client):
        url = reverse("accounts:ApiV1:account_urls:register")
        api_client.force_authenticate(user=common_user)
        data = {
            "email": "user@example.com",
            "password": "Abcd@1234",
            "password1": "Abcd@1234",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

        # assertion of returned email value
        assert "user@example.com" in response.data["email"]

        # wrong data with duplicate user registration
        data = {
            "email": "user@example.com",
            "password": "Abcd@1234",
            "password1": "Abcd@1234",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

        # wrong data with low complexity password
        data = {"email": "user@example.com", "password": "1234", "password1": "1234"}
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_jwt_login_success(self, api_client, common_user):
        url = reverse("accounts:ApiV1:account_urls:jwt-create")
        api_client.force_authenticate(user=common_user)
        data = {
            "email": "ali@abc.com",
            "password": "ali@1234",
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert "access" in response.data

    def test_jwt_login_fail(self, api_client, common_user):
        url = reverse("accounts:ApiV1:account_urls:jwt-create")
        api_client.force_authenticate(user=common_user)
        data = {
            "email": "nonexistent@abc.com",
            "password": "wrongpass",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_get_account_creation_200_status(self, api_client, common_user):
        url = reverse("accounts:ApiV1:account_urls:jwt-create")
        api_client.force_authenticate(user=common_user)
        data = {
            "email": "ali@abc.com",
            "password": "ali@1234",
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert "access" in response.data

    def test_get_account_creation_401_status(self, api_client):
        url = reverse("accounts:ApiV1:account_urls:jwt-create")
        # api_client.force_authenticate(user=common_user)
        data = {
            "email": "ali@abc.com",
            "password": "ali@1234",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_get_account_token_create(self, api_client, common_user):
        url = reverse("accounts:ApiV1:account_urls:jwt-create")
        api_client.force_authenticate(user=common_user)
        data = {
            "email": "ali@abc.com",
            "password": "ali@1234",
        }
        response = api_client.post(url, data)

        access_token = response.data["access"]
        activation_url = reverse(
            "accounts:ApiV1:account_urls:activation",
            kwargs={"token": access_token},  # یا args=[access_token]
        )
        response = api_client.get(activation_url)
        assert "verified" in response.data["details"]

    def test_get_account_token_notcreate(self, api_client, common_user):
        # ساخت یک توکن کاملاً نامعتبر (بدون دستکاری توکن معتبر)
        invalid_token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c" + "InvalidPart")

        activation_url = reverse(
            "accounts:ApiV1:account_urls:activation", kwargs={"token": invalid_token}
        )
        response = api_client.get(activation_url)
        assert "token is not valid" in response.data["details"]

    def test_expired_token_activation(self, api_client, expired_token):
        # ساخت توکن منقضی‌شده
        activation_url = reverse(
            "accounts:ApiV1:account_urls:activation", kwargs={"token": expired_token}
        )
        response = api_client.get(activation_url)

        # بررسی پاسخ
        # print(response.data,'////////////////////////////')
        error_message = (
            response.data.get("details", "") or response.data.get("detail", "") or response.data.get("error", "")).lower()
        assert (
            response.status_code == 400
        )  # یا کد دیگری که برای توکن منقضی‌شده تعیین کرده‌اید
        assert "token has been expired" in error_message

    # def test_get_account_token_verified(self, api_client, common_user):
    #     url = reverse("accounts:ApiV1:account_urls:jwt-create")
    #     api_client.force_authenticate(user=common_user)
    #     data = {
    #         "email": "ali@abc.com",
    #         "password": "ali@1234",
    #     }
    #     response = api_client.post(url, data)

    #     access_token = response.data["access"]
    #     activation_url = reverse(
    #         "accounts:ApiV1:account_urls:jwt-verify")+ f"?token={access_token}"
    #     response = api_client.post(activation_url)

    #     response_message = (response.data.get("details", "") or response.data.get("detail", "") or response.data.get("error", "")).lower()
    #     print(response_message, '////////////////////////////', response.data)
    #     assert "" in response_message
