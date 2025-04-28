from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from accounts.api.v1.views import RegisterApiView, CustomTokenObtainPairView, ActivationResendApiView, ProfileApiView
# Create your tests here.

class TestUrl(SimpleTestCase):

    def test_account_register_url_resolve(self):
        url = reverse('accounts:ApiV1:account_urls:register')
        self.assertEqual(resolve(url).func.view_class,RegisterApiView)

    def test_account_create_jwt_url_resolve(self):
        url = reverse('accounts:ApiV1:account_urls:jwt-create')
        self.assertEqual(resolve(url).func.view_class,CustomTokenObtainPairView)

    def test_account_activation_resend_resolve(self):
        url = reverse('accounts:ApiV1:account_urls:activation-resend')
        self.assertEqual(resolve(url).func.view_class,ActivationResendApiView)

    def test_account_profile_resolve(self):
        url = reverse('accounts:ApiV1:profile_urls:profile')
        self.assertEqual(resolve(url).func.view_class,ProfileApiView)    

