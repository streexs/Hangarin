from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from hangarin.forms import TaskForm, PriorityForm, CategoryForm, NoteForm, SubTaskForm
from django.urls import reverse_lazy
from hangarin.models import Task, Priority, Category, Note, SubTask
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, ListView):   
    model = Task
    context_object_name = 'home'
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics for dashboard
        context['total_tasks'] = Task.objects.count()
        context['pending_tasks'] = Task.objects.filter(status='Pending').count()
        context['in_progress_tasks'] = Task.objects.filter(status='In Progress').count()
        context['completed_tasks'] = Task.objects.filter(status='Completed').count()
        
        # Additional statistics
        context['total_categories'] = Category.objects.count()
        context['total_priorities'] = Priority.objects.count()
        context['total_notes'] = Note.objects.count()
        context['total_subtasks'] = SubTask.objects.count()
        
        # Tasks created this year
        current_year = datetime.now().year
        context['tasks_this_year'] = Task.objects.filter(
            created_at__year=current_year
        ).count()
        
        return context

#tasklist 
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Task.objects.all()
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(status__icontains=query) |
                Q(category__name__icontains=query) |
                Q(priority__name__icontains=query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by category
        category_filter = self.request.GET.get('category')
        if category_filter:
            queryset = queryset.filter(category_id=category_filter)
        
        # Filter by priority
        priority_filter = self.request.GET.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority_id=priority_filter)
        
        # Sorting/Ordering
        ordering = self.request.GET.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        context['status_choices'] = ['Pending', 'In Progress', 'Completed']
        return context

#taskcreate 
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task-list")
    
    def form_valid(self, form):
        print("Form is valid - saving task")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form is invalid - errors:", form.errors)
        return super().form_invalid(form)

#taskupdate
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')   

#taskdelete    
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')

#prioritylist
class PriorityList(ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'priority_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Priority.objects.all()
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))
        
        # Sorting/Ordering
        ordering = self.request.GET.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset

#prioritycreate
class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")

#priorityupdate
class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

#prioritydelete
class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'priority_del.html'
    success_url = reverse_lazy('priority-list')

#categorylist
class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Category.objects.all()
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))
        
        # Sorting/Ordering
        ordering = self.request.GET.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset

#categorycreate
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")

#categoryupdate
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

#categorydelete
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_del.html'
    success_url = reverse_lazy('category-list')

#notelist
class NoteList(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Note.objects.all()
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(content__icontains=query) |
                Q(task__title__icontains=query)
            )
        
        # Filter by task
        task_filter = self.request.GET.get('task')
        if task_filter:
            queryset = queryset.filter(task_id=task_filter)
        
        # Sorting/Ordering
        ordering = self.request.GET.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context

#notecreate
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note-list")

#noteupdate
class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

#notedelete
class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_del.html'
    success_url = reverse_lazy('note-list')

#subtasklist
class SubTaskList(ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'subtask_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = SubTask.objects.all()
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(status__icontains=query) |
                Q(parent_task__title__icontains=query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by parent task
        task_filter = self.request.GET.get('task')
        if task_filter:
            queryset = queryset.filter(parent_task_id=task_filter)
        
        # Sorting/Ordering
        ordering = self.request.GET.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['status_choices'] = ['Pending', 'In Progress', 'Completed']
        return context

#subtaskcreate
class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy("subtask-list")

    def dispatch(self, request, *args, **kwargs):
        # Get the parent task from URL if provided (optional)
        task_pk = kwargs.get('task_pk')
        self.parent_task = get_object_or_404(Task, pk=task_pk) if task_pk else None
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        # Pre-fill the parent_task field if task was provided
        initial = super().get_initial()
        if self.parent_task:
            initial['parent_task'] = self.parent_task
        return initial

    def form_valid(self, form):
        # Ensure parent_task is set if provided
        if self.parent_task:
            form.instance.parent_task = self.parent_task
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Pass parent_task to template if available
        context = super().get_context_data(**kwargs)
        if self.parent_task:
            context['parent_task'] = self.parent_task
        return context

#subtaskupdate
class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

#subtaskdelete
class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_del.html'
    success_url = reverse_lazy('subtask-list')