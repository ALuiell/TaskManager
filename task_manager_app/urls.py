from django.urls import path
import task_manager_app.views as views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("load-projects/", views.load_projects_view, name="load_project_list"),
    path("add-project/", views.add_project_view, name="add_project"),
    path('update-project/<int:project_id>/', views.update_project_view, name="update_project"),
    path('delete-project/<int:project_id>/', views.delete_project_view, name="delete_project"),
    path('load-tasks/<int:project_id>/', views.load_tasks_view, name="load_tasks"),
    path("add-task/<int:project_id>/", views.add_task_view, name="add_task"),
    path('update-task/<int:task_id>/', views.update_task_view, name="update_task"),
    path('get-update-task-form/<int:task_id>/', views.get_update_task_form_view, name="get_task_update_form"),
    path('delete-task/<int:task_id>/', views.delete_task_view, name="delete_task"),
]