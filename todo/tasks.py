from celery import shared_task
from django.utils import timezone
from .models import Task


@shared_task
def delete_completed_tasks():
    # پاک کردن تسک‌هایی که وضعیت "انجام‌شده" دارند
    deleted_count, _ = Task.objects.filter(completed=True).delete()
    return f"{deleted_count} tasks deleted successfully."
