from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path("load-projects/", load_projects_view, name="load_projects"),
    path("add-project/", add_project_view, name="add_project"),
    path('update-project/<int:project_id>/', update_project_view, name="update_project"),
    path('delete-project/<int:project_id>/', delete_project_view, name="delete_project"),
    # path('load-tasks', load_tasks_view, name="load_tasks"),
    # path("add-task/<int:project_id>/", add_task_view, name="add_task"),
    # path('update-task/<int:task_id>/', update_task_view, name="update_task"),
    # path('change-priority-task/<int:task_id>/', change_priority_task_view, name="change_priority_task"),
    # path('delete-task/<int:task_id>/', delete_task_view, name="delete_task"),
]