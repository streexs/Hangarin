from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from app.models import Category, Priority, Task, SubTask, Note

class Command(BaseCommand):
    help = 'Create initial data for the web application'

    def handle(self, *args, **kwargs):
        self.create_task(10)
        self.create_notes(10)
        self.create_subtask(10)

    def create_task(self, count):
        fake = Faker()

        categories = Category.objects.all()
        priorities = Priority.objects.all()

        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please create some Category objects first.'))
            return
        if not priorities.exists():
            self.stdout.write(self.style.ERROR('No priorities found. Please create some Priority objects first.'))
            return

        for _ in range(count):
            Task.objects.create(    
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_between()),
                status=fake.random_element(
                    elements=['Pending', 'In Progress', 'Completed']
                    ),
                category=categories.order_by('?').first(),
                priority=priorities.order_by('?').first(),
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for task created successfully.'))
    
    def create_notes(self, count):
        fake = Faker()
        tasks = Task.objects.all()
        if not tasks.exists():
            self.stdout.write(self.style.ERROR('No tasks found. Please create some Task objects first.'))
            return

        for _ in range(count):
            task = tasks.order_by('?').first()
            if not task:
                self.stdout.write(self.style.ERROR('No valid Task found for Note. Skipping.'))
                continue
            Note.objects.create(    
                task=task,
                content=fake.paragraph(nb_sentences=3),
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for note created successfully.'))

    def create_subtask(self, count):
        fake = Faker()
        tasks = Task.objects.all()
        if not tasks.exists():
            self.stdout.write(self.style.ERROR('No tasks found. Please create some Task objects first.'))
            return

        for _ in range(count):
            parent_task = tasks.order_by('?').first()
            if not parent_task:
                self.stdout.write(self.style.ERROR('No valid Task found for SubTask. Skipping.'))
                continue
            SubTask.objects.create(    
                parent_task=parent_task,
                title=fake.sentence(nb_words=5),
                status=fake.random_element(
                    elements=['Pending', 'In Progress', 'Completed']
                ),
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for subtask created successfully.'))