from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
import random

from accounts.models import User, Profile
from todo.models import Task


class Command(BaseCommand):
    help = "Insert dummy data to DB"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):

        # generate user and fill his profile (in necessity uncomment statements)

        user = User.objects.create_user(
            email=self.faker.email(),
            password="Abcd@1234",
            is_active=True,
            is_staff=random.choice([True, False]),
            is_verified=random.choice([True, False]),
        )
        profile = Profile.objects.get(user=user)
        profile.first_name = self.faker.first_name()
        profile.last_name = self.faker.last_name()
        profile.bio = self.faker.paragraph(nb_sentences=3)
        profile.save()

        number_of_users = User.objects.count()
        for _ in range(5):
            # select random user
            user_random_paint = User.objects.all()[
                random.randint(0, number_of_users - 1)
            ]
            Task.objects.create(
                user=user_random_paint,
                task_name=self.faker.text(max_nb_chars=20),
                completed=random.choice([True, False]),
                published_at=timezone.now(),
            )
