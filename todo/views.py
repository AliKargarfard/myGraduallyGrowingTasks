from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Task
from .forms import TaskUpdateForm


class ListTask(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/task_list.html"

    def get_queryset(self):
        print(self.request.__dict__, "****************")
        return self.model.objects.filter(user=self.request.user)


class ListTaskApi(TemplateView):
    template_name = "todo/task_list_api.html"


class TaskDetailView(DetailView):
    model = Task
    template_name = "todo/task_details.html"


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["task_name"]
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        # print(self.request.user,'-',form.instance.user,'-', self.context_object_name)
        return super(CreateTask, self).form_valid(form)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("todo:task_list")
    form_class = TaskUpdateForm
    template_name = "todo/update_task.html"


""" Mark a task as a Completed task """


class CompletedTask(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.completed = True
        object.save()
        return redirect(self.success_url)


""" Undo the completed task """


class UnCompletedTask(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.completed = False
        object.save()
        return redirect(self.success_url)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task_name"
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
