"""# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomPagination
# from rest_framework.response import Response

# افزودن ماژول فیلترینگ داده ها
from django_filters.rest_framework import DjangoFilterBackend
# ماژول سرچ و جستجو در فیلترها
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework import viewsets

from .serializers import TaskSerializer
from ...models import Task
# from django.shortcuts import get_object_or_404


class TaskModelViewSet(viewsets.ModelViewSet):

    # (Owner)صدور مجوز تغییر فقط برای کاربر ایجاد کننده پست
    # (IsOwnerOrReadOnly)و بقیه کاربران تنها مشاهده محتوای پست
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    # (ordering)ایجاد امکان فیلترینگ رکوردها و جستجو و مرتب سازی
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # انتخاب فیلدهای مورد نظر برای فیلترینگ
    filterset_fields = ['user', 'task_name', 'created_at', 'updated_at']
    # انتخاب فیلدهای مورد نظر برای جستجو
    search_fields = ['task_name', 'user']
    # انتخاب فیلدهای مورد نظر برای مرتب سازی
    ordering_fields = ['task_name', 'created_at']
    # paginations.py ایجاد امکان صفحه بندی برگرفته از فایل
    pagination_class = CustomPagination

"""

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework.permissions import (
    # IsAuthenticated,
    # IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .serializers import TaskSerializer
from ...models import Task

# from rest_framework import status
from rest_framework.generics import (
    # GenericAPIView,
    # ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

# from rest_framework import mixins
# from django.shortcuts import get_object_or_404


"""
@api_view(["GET","POST"])
@permission_classes([IsAdminUser])
def taskList(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        # instead of (if serializer.is_valid(): ...)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)


@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def taskDetail(request, id):
    # try:
    #     task = Task.objects.get(pk=id)
    #     print(task.__dict__)
    #     serializer = TaskSerializer(task)
    #     return Response(serializer.data)
    # except Task.DoesNotExist:
    #     return Response({'detail':'Task does not exist!'},status=status.HTTP_404_NOT_FOUND)

    task = get_object_or_404(Task, pk=id)
    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = TaskSerializer(task,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        # print (task.task_name)
        task.delete()
        return Response({"detail": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
"""


"""class TaskList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # add input html form fields to the list of post
    serializer_class = TaskSerializer
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TaskDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer

    def get(self, request, id):
        task = get_object_or_404(Task, pk=id)
        serializer = self.serializer_class(task)
        return Response(serializer.data)

    def put(self, request, id):
        task = get_object_or_404(Task, pk=id)
        serializer = self.serializer_class(task,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        task = get_object_or_404(Task, pk=id)
        task.delete()
        return Response({"detail": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
"""


class TaskList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
