from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from hangarin.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = 'Populate database with fake records for Task, Note, and SubTask only.'

    def handle(self, *args, **kwargs):
        self.add_tasks(10)
        self.add_notes(10)
        self.add_subtasks(10)

    def add_tasks(self, count):
        fake = Faker()
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())
        statuses = ["Pending", "In Progress", "Completed"]
        for _ in range(count):
            Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=statuses),
                priority=fake.random_element(elements=priorities),
                category=fake.random_element(elements=categories),
            )
        self.stdout.write(self.style.SUCCESS('Tasks added.'))

    def add_notes(self, count):
        fake = Faker()
        tasks = list(Task.objects.all())
        for _ in range(count):
            Note.objects.create(
                content=fake.paragraph(nb_sentences=3),
                task=fake.random_element(elements=tasks),
            )
        self.stdout.write(self.style.SUCCESS('Notes added.'))

    def add_subtasks(self, count):
        fake = Faker()
        tasks = list(Task.objects.all())
        statuses = ["Pending", "In Progress", "Completed"]
        for _ in range(count):
            SubTask.objects.create(
                title=fake.sentence(nb_words=5),
                status=fake.random_element(elements=statuses),
                parent_task=fake.random_element(elements=tasks),
            )
        self.stdout.write(self.style.SUCCESS('SubTasks added.'))
