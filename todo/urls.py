from django.urls import path, include
from .views import (
    ListTask,
    ListTaskApi,
    TaskDetailView,
    CreateTask,
    CompletedTask,
    UnCompletedTask,
    UpdateTask,
    DeleteTaskView,
)

app_name = "todo"

urlpatterns = [
    path("todo/", ListTask.as_view(), name="task_list"),
    path("todo/api/", ListTaskApi.as_view(), name="list_tasks"),
    path("todo/<int:pk>", TaskDetailView.as_view(), name="task_detail"),
    path("create/", CreateTask.as_view(), name="create_task"),
    path("delete/<int:pk>/", DeleteTaskView.as_view(), name="delete_task"),
    path("update/<int:pk>/", UpdateTask.as_view(), name="update_task"),
    path("completed/<int:pk>/", CompletedTask.as_view(), name="task_done"),
    path("uncompleted/<int:pk>/", UnCompletedTask.as_view(), name="task_undone"),
    path("todo/api/v1/", include("todo.api.v1.urls")),
]
