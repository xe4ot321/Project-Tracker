from django.shortcuts import render, redirect
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "index.html", {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        project = request.POST.get('project')
        priority = request.POST.get('priority')
        date = request.POST.get('date') or None

        Task.objects.create(
            user=request.user,
            name=name,
            description=description,
            project=project,
            priority=priority,
            date=date
        )
        return redirect('create_task')
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'index.html', {'tasks': tasks})


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)