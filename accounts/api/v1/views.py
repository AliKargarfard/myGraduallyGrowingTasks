from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from ...models import Profile
from .serializers import(
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenOptainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
)
from .utils import EmailThread


User = get_user_model()


class RegisterApiView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)

            # sending email using threading
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "ali@abc.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDeleteAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenOptainPairSerializer
    

class ChangePasswordView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        object = self.request.user
        return object

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        object = get_object_or_404(queryset, user=self.request.user)
        return object


class EmailTestView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        # send_mail(
        #     "Subject here",
        #     "Here is the message.",
        #     "from@example.com",
        #     ["to@example.com"],
        #     fail_silently=False,
        # )

        # using send_mail() function
        # send_mail('email/hello.tpl', {'Name': 'Ali'}, 'ali@abc.com', ['akargarfard@gmail.com'])

        # More control with EmailMessage class
        # message = EmailMessage('email/hello.tpl', {'Name': 'Ali'}, 'ali@abc.com', to=['akargarfard@gmail.com'])
        # message.send()

        self.email = "ali@abc.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        # sending email using threading
        email_obj = EmailMessage(
            "email/hello.tpl", {"token": token}, "ali@abc.com", to=[self.email]
        )
        EmailThread(email_obj).start()

        return Response("Email sent")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        # Token generated by simple-jwt-django-rest-framework or any
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"details": "this account has already been verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "your account has been verified and activated successfully"}
        )
        return Response(token)


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        # sending email using threading
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "ali@abc.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "resend activation token has been sent"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
