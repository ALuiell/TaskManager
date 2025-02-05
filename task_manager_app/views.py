from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Task



# Create your views here.
def home_view(request):
    return render(request, 'task_manager_app/home.html')


def load_projects_view(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, "task_manager_app/projects_list.html", {"projects": projects})



def add_project_view(request):
    if request.method == "POST":
        project_name = request.POST.get("name")
        if not project_name:
            return HttpResponseBadRequest("Project name is required.")

        Project.objects.create(name=project_name, user=request.user)
        projects = Project.objects.filter(user=request.user)
        return render(request, "task_manager_app/projects_list.html", {"projects": projects})

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



# def load_tasks_view(request, project_id):
#     project = get_object_or_404(Project, id=project_id, user=request.user)
#     tasks = project.tasks.all()
#     return render(request, "task_manager_app/tasks_list.html", {"tasks": tasks, "project": project})
#

# def add_task_view(request, project_id):
#     if request.method == "POST":
#         project = get_object_or_404(Project, id=project_id, user=request.user)
#         task_name = request.POST.get("name")
#
#         if not task_name:
#             return HttpResponseBadRequest("Task name is required.")
#
#         Task.objects.create(name=task_name, project=project)
#
#         tasks = project.tasks.all()
#         return render(request, "task_manager_app/tasks_list.html", {"tasks": tasks, "project": project})
#
#
# def update_task_view(request):
#     pass
#
# def change_priority_task_view(request):
#     pass
#
# def delete_task_view(request):
#     pass