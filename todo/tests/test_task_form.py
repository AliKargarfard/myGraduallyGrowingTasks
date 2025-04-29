from django.test import TestCase

from todo.forms import TaskUpdateForm


class TestTaskForm(TestCase):

    def test_Task_form_with_valid_data(self):
        form = TaskUpdateForm(
            data={
                "task_name": "test Task",
                "completed": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_post_form_with_no_data(self):
        form = TaskUpdateForm(data={})
        self.assertFalse(form.is_valid())
