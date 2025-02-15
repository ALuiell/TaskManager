from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from datetime import datetime


# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "task_manager_app/home.html"

@login_required
def load_projects_view(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, "task_manager_app/projects_list.html", {"projects": projects})


@login_required
def add_project_view(request):
    if request.method == "POST":
        project_name = request.POST.get("name")
        if not project_name:
            return HttpResponseBadRequest("Project name is required.")

        project = Project.objects.create(name=project_name, user=request.user)

        return render(request, "task_manager_app/project_item.html", {"project": project})

@login_required
def update_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == "POST":
        project_name = request.POST.get("name")
        if not project_name:
            return HttpResponseBadRequest("Project name is required.")

        project.name = project_name
        project.save()

        return render(request, "task_manager_app/project_item.html", {"project": project})

@login_required
def delete_project_view(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=project_id, user=request.user)
        project.delete()

    # projects = Project.objects.filter(user=request.user)
    # return render(request, "task_manager_app/projects_list.html", {"projects": projects})
    return HttpResponse("")



def load_tasks_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = project.tasks.all()
    priority_choices = Task.PRIORITY_CHOICES
    task_status_choices = Task.STATUS_CHOICES
    now = datetime.now()
    hours_left_dict = {}
    for task in tasks:
        if task.deadline:
            now_with_tz = now.astimezone(task.deadline.tzinfo)
            delta = task.deadline - now_with_tz
            hours = delta.total_seconds() // 3600
            hours_left_dict[task.id] = int(hours)


    return render(request, "task_manager_app/tasks_list.html", {"tasks": tasks, "project": project,
                                                                "priority_choices": priority_choices,
                                                                "task_status_choices": task_status_choices,
                                                                "now":datetime.now(),
                                                                "hours_left_dict": hours_left_dict})

@login_required
def add_task_view(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id, user=request.user)
        task_name = request.POST.get("name")
        task_priority = request.POST.get("priority")
        task_deadline = request.POST.get("deadline")
        if not task_name:
            return HttpResponseBadRequest("Task name is required.")

        task_priority = int(task_priority) if task_priority and task_priority.isdigit() else 2

        if task_deadline:
            task_deadline = datetime.strptime(task_deadline, "%Y-%m-%dT%H:%M")
        else:
            task_deadline = None

        Task.objects.create(name=task_name, project=project, priority=task_priority, deadline=task_deadline)

        return redirect('load_tasks', project_id=project_id)

@login_required
def update_task_view(request, task_id):
    if request.method == "POST":
        task_name = request.POST.get("name")
        task_priority = request.POST.get("priority")
        task_deadline = request.POST.get("deadline")
        task_status = request.POST.get("status")

        task = get_object_or_404(Task, id=task_id)
        if task.project.user != request.user:
            return HttpResponseForbidden("Access denied.")
        if (task_name, task_priority, task_status, task_deadline) != (task.name, task.priority, task.status, task.deadline):
            task.name = task_name
            task.priority = int(task_priority)
            task.status = task_status
            task.deadline = datetime.strptime(task_deadline, "%Y-%m-%dT%H:%M") if task_deadline != "" else None
            task.save()
            return redirect('load_tasks', project_id=task.project.id)


def get_update_task_form_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    return render(request, "task_manager_app/update_task_form.html", {"task": task, "now":datetime.now()})

@login_required
def delete_task_view(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)

        if task.project.user != request.user:
            return HttpResponseForbidden("Access denied.")

        project = task.project
        task.delete()

        return redirect('load_tasks', project_id=project.id)

