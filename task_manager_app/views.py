from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import Project, Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "task_manager_app/home.html"


def load_projects_view(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, "task_manager_app/projects_list.html", {"projects": projects})

# add_project view for the version where the project list logic
# works based on individual project_item templates instead of reloading the entire list.
@login_required
def add_project_view(request):
    if request.method == "POST":
        project_name = request.POST.get("name")
        if not project_name:
            return HttpResponseBadRequest("Project name is required.")

        project = Project.objects.create(name=project_name, user=request.user)

        return render(request, "task_manager_app/project_item.html", {"project": project})

def update_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == "POST":
        project_name = request.POST.get("name")
        if not project_name:
            return HttpResponseBadRequest("Project name is required.")

        project.name = project_name
        project.save()

        projects = Project.objects.filter(user=request.user)
        return render(request, "task_manager_app/projects_list.html", {"projects": projects})


def delete_project_view(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=project_id, user=request.user)
        project.delete()

    projects = Project.objects.filter(user=request.user)
    return render(request, "task_manager_app/projects_list.html", {"projects": projects})



def load_tasks_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = project.tasks.all()
    return render(request, "task_manager_app/tasks_list.html", {"tasks": tasks, "project": project})


def add_task_view(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id, user=request.user)
        task_name = request.POST.get("name")

        if not task_name:
            return HttpResponseBadRequest("Task name is required.")

        Task.objects.create(name=task_name, project=project)

        tasks = project.tasks.all()
        return render(request, "task_manager_app/tasks_list.html", {"tasks": tasks, "project": project})
#
#
# def update_task_view(request):
#     pass
#
# def change_priority_task_view(request):
#     pass
#
@login_required
def delete_task_view(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)

        if task.project.user != request.user:
            return HttpResponseForbidden("You do not have permission to delete this task.")

        project = task.project
        task.delete()

        tasks = Task.objects.filter(project=project)
        return render(request, "task_manager_app/tasks_list.html", {"tasks": tasks, "project": project})

