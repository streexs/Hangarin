from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Priority(BaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name

class Category(BaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Categorys"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Task(BaseModel):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    deadline = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed"),
        ],
        default="Pending"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.status})"

class Note(BaseModel):
    content = models.CharField(max_length=150)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"{self.content[:30]}... for {self.task.title}"

class SubTask(BaseModel):
    title = models.CharField(max_length=150)
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed"),
        ],
        default="Pending"
    )
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")

    class Meta:
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"

    def __str__(self):
        return f"{self.title} ({self.status}) - {self.parent_task.title}"
