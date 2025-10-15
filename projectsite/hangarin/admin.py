from django.contrib import admin

from .models import Priority, Category, Task, Note, SubTask

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ("title", "status")
    show_change_link = True

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    fields = ("content", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Priority)
class PriotityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "deadline", "priority", "category", "status",)
    search_fields = ("title", "description",)
    list_filter = ("status", "priority", "category",)

    inlines = [SubTaskInline, NoteInline]

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task", "content","created_at",)
    search_fields = ("cpntent",)
    list_filter = ("created_at",)

@admin.register(SubTask)
class SubTask(admin.ModelAdmin):
    list_display = ("title", "status", "parent_task",)
    search_fields = ("title"    ,)
    list_filter = ("status",)
    